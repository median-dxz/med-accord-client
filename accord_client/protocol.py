import json
import sys
import typing
from dataclasses import dataclass
from enum import Enum

from PyQt6.QtCore import QObject, pyqtSignal

from accord_client.model import action


class ProtocolEncoding(Enum):
    UTF8 = "utf8"
    BINARY = "binary"


@dataclass
class ProtocolHeader:
    ContentLength: int
    ContentMime: str
    ContentEncoding: ProtocolEncoding
    Action: action.ActionType


def protocol_header(data: dict):
    return ProtocolHeader(
        Action=action.ActionType(data["Action"]),
        ContentEncoding=ProtocolEncoding(data["ContentEncoding"]),
        ContentLength=int(data["ContentLength"]),
        ContentMime=str(data["ContentMime"]),
    )


class ProtocolHeaderEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ProtocolHeader):
            return {
                "Action": o.Action.value,
                "ContentEncoding": o.ContentEncoding.value,
                "ContentLength": o.ContentLength,
                "ContentMime": o.ContentMime,
            }
        return json.JSONEncoder.default(self, o)


class ProtocolData(QObject):
    readyConsume = pyqtSignal(ProtocolHeader, bytearray)

    def __init__(self, chunk) -> None:
        super().__init__()
        self.fixedLength: int = 0
        self.header: typing.Optional[ProtocolHeader] = None
        self.body: typing.Optional[bytearray] = None
        self.chunk = chunk
        self.consumed = False

    def onData(self, data: bytearray):
        self.chunk += data
        buf = bytearray(self.chunk)
        bytesRead = 0
        bytesToRead = 4

        if (self.fixedLength == 0) & (len(buf) >= bytesToRead):
            self.fixedLength = int.from_bytes(
                buf[bytesRead : bytesRead + bytesToRead],
                byteorder=sys.byteorder,
                signed=False,
            )
            bytesRead += bytesToRead

        if self.fixedLength != 0:
            bytesToRead = self.fixedLength

        if (self.header is None) & (len(buf) - bytesRead >= bytesToRead):
            self.header = json.loads(
                buf[bytesRead : bytesRead + bytesToRead].decode("utf-8"),
                object_hook=protocol_header,
            )
            bytesRead += bytesToRead

        if not self.header is None:
            bytesToRead = self.header.ContentLength

        if (self.body is None) & (len(buf) - bytesRead >= bytesToRead):
            self.body = buf[bytesRead : bytesRead + bytesToRead]
            bytesRead += bytesToRead
            self.readyConsume.emit(self.header, self.body)
            self.consumed = True

        self.chunk = buf[bytesRead:]
