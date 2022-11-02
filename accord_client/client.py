import json
import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QAbstractSocket, QHostAddress, QTcpSocket

import accord_client.model.action as Action
import accord_client.model.data as AccordData
import accord_client.model.model as AccordModel
from accord_client import DataBuilder, SignalWaiter, protocol, settings
from accord_client.member import MemberController

member = MemberController()


class ClientController(QObject):
    _instance = None

    emitDisconnected = pyqtSignal()
    emitReceiveCtrlMsg = pyqtSignal(str, str)
    emitUpdateMembersList = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()

        self._socket = QTcpSocket()
        self._socket.readyRead.connect(self.receive)
        self._socket.disconnected.connect(self.disconnected)

        self.init()

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = QObject.__new__(cls, *args, **kw)
        return cls._instance

    def init(self):
        self.protocolData = protocol.ProtocolData(bytearray())
        self.serverData = AccordData.ServerData()

    def connect(self):
        [host, port] = settings.getValue("AccordServer", ["host", "port"])
        port = int(port)

        if self._socket.state() == QAbstractSocket.SocketState.ConnectedState:
            return

        print(f"[ServerController]: Try Connect {host}:{port}")

        self._socket.setSocketOption(QAbstractSocket.SocketOption.KeepAliveOption, 1)
        self._socket.connectToHost(QHostAddress(host), port)
        self.protocolData.readyConsume.connect(self.consume)

    def disconnected(self):
        print(f"[Accord]: Close Connection")
        self.init()
        self.emitDisconnected.emit()

    def receive(self):
        print(f"[Accord]: Client<<Server")
        if self.protocolData.consumed:
            chunk = self.protocolData.chunk
            self.protocolData = protocol.ProtocolData(chunk)
            self.protocolData.readyConsume.connect(self.consume)

        self.protocolData.onData(self._socket.readAll())  # type: ignore

    def leave(self):
        # print(self._socket.state())
        if self.serverData.hash == "":
            return
        self.request(Action.ActionType.LEAVE)
        self._socket.disconnectFromHost()

    def enter(self, data: AccordData.ServerData):
        self.serverData = data
        self.promise = SignalWaiter(self._socket.connected, self.connect)  # type: ignore
        self.promise.then(lambda: self.request(Action.ActionType.ENTER))

    def consume(self, header: protocol.ProtocolHeader, body: bytes):
        decode_body = body.decode("utf8")
        match header.Action:
            case Action.ActionType.UPDATE_MEMBERS:
                memberList = json.loads(decode_body, object_hook=DataBuilder.update_members_list)
                print(memberList)
                self.emitUpdateMembersList.emit(memberList)
            case _:
                self.emitReceiveCtrlMsg.emit(decode_body, header.Action.value)
        print(decode_body, header.Action)

    def request(self, action: Action.ActionType):
        body = b""
        content = ""
        match action:
            case Action.ActionType.ENTER:
                content = json.dumps(
                    Action.ActionEnter(
                        serverHash=self.serverData.hash,
                        memberHash=member.hash,
                        avatar=member.avatar,
                        name=member.name,
                    ),
                    cls=Action.AccordActionEncoder,
                    ensure_ascii=False,
                )
            case Action.ActionType.LEAVE:
                content = "离开服务器"

        body = content.encode("utf8")
        header = protocol.ProtocolHeader(
            Action=action,
            ContentEncoding=protocol.ProtocolEncoding.UTF8,
            ContentLength=len(body),
            ContentMime="application/json",
        )
        headerBuffer = json.dumps(header, cls=protocol.ProtocolHeaderEncoder).encode("utf-8")

        fixedLength = len(headerBuffer).to_bytes(4, sys.byteorder, signed=False)
        self._socket.write(fixedLength + headerBuffer + body)
