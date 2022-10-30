import json
import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QAbstractSocket, QHostAddress, QTcpSocket

import accord_client.model.AccordAction as Action
from accord_client import globalSettings
from accord_client.helper import data_builder as DataBuilder
from accord_client.helper.signal_waiter import SignalWaiter
from accord_client.model.AccordServer import *
from accord_client.provider import member_controller as MemberController
from accord_client.provider import protocol_controller as ProtocolController

user = MemberController.MemberController()


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
        self.protocolData = ProtocolController.ProtocolData(bytearray())
        self.serverData = ServerData()

    def connect(self):
        globalSettings.beginGroup("AccordServer")
        host = globalSettings.value("host")
        port = int(globalSettings.value("port"))
        globalSettings.endGroup()

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
            self.protocolData = ProtocolController.ProtocolData(chunk)
            self.protocolData.readyConsume.connect(self.consume)

        self.protocolData.onData(self._socket.readAll())  # type: ignore

    def leave(self):
        # print(self._socket.state())
        if self.serverData.hash == "":
            return
        self.request(Action.ActionType.LEAVE)
        self._socket.disconnectFromHost()

    def enter(self, data: ServerData):
        self.serverData = data
        self.promise = SignalWaiter(self._socket.connected, self.connect)  # type: ignore
        self.promise.then(lambda: self.request(Action.ActionType.ENTER))

    def consume(self, header: ProtocolDataHeader, body: bytes):
        match header.Action:
            case Action.ActionType.UPDATE_MEMBERS:
                self.emitUpdateMembersList.emit(DataBuilder.update_members_list(json.loads(body.decode())))
            case _:
                self.emitReceiveCtrlMsg.emit(body.decode(), header.Action.value)
        print(body.decode(), header.Action)

    def request(self, action: Action.ActionType):
        body = b""
        content = ""
        match action:
            case Action.ActionType.ENTER:
                content = json.dumps(
                    Action.ActionEnter(
                        serverHash=self.serverData.hash,
                        memberHash=user.getMemberHash(),
                        avatar=user.getAvatar(),
                        name=user.getName(),
                    ),
                    cls=Action.AccordActionEncoder,
                    ensure_ascii=False,
                )
            case Action.ActionType.LEAVE:
                content = "离开服务器"

        body = content.encode("utf8")
        header = ProtocolDataHeader(
            Action=action,
            ContentEncoding=ProtocolDataEncoding.UTF8,
            ContentLength=len(body),
            ContentMime="application/json",
        )
        headerBuffer = json.dumps(header, cls=DataBuilder.ProtocolDataHeaderEncoder).encode("utf-8")

        fixedLength = len(headerBuffer).to_bytes(4, sys.byteorder, signed=False)
        self._socket.write(fixedLength + headerBuffer + body)
