import json
import sys
import typing

from PyQt6.QtCore import QObject, pyqtSignal

from accord_client.model import AccordServer
from accord_client.helper import data_builder as DataBuilder


class ProtocolData(QObject):
    readyConsume = pyqtSignal(AccordServer.ProtocolDataHeader, bytearray)

    def __init__(self, chunk) -> None:
        super().__init__()
        self.fixedLength: int = 0
        self.header: typing.Optional[AccordServer.ProtocolDataHeader] = None
        self.body: typing.Optional[bytearray] = None
        self.chunk = chunk
        self.consumed = False

    def onData(self, data: bytearray):
        self.chunk += data
        buf = bytearray(self.chunk)
        bytesRead = 0
        bytesToRead = 4

        if (self.fixedLength == 0) & (len(buf) >= bytesToRead):
            self.fixedLength = int.from_bytes(buf[bytesRead:bytesRead + bytesToRead], byteorder=sys.byteorder, signed=False)
            bytesRead += bytesToRead

        if (self.fixedLength != 0):
            bytesToRead = self.fixedLength

        if (self.header is None) & (len(buf) - bytesRead >= bytesToRead):
            header = json.loads(buf[bytesRead:bytesRead + bytesToRead].decode('utf-8'))
            self.header = DataBuilder.protocol_data_header(header)
            bytesRead += bytesToRead

        if (not self.header is None):
            bytesToRead = self.header.ContentLength

        if (self.body is None) & (len(buf) - bytesRead >= bytesToRead):
            self.body = buf[bytesRead:bytesRead + bytesToRead]
            bytesRead += bytesToRead
            self.readyConsume.emit(self.header, self.body)
            self.consumed = True

        self.chunk = buf[bytesRead:]
