import json
import sys

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QAbstractSocket, QHostAddress, QTcpSocket

import accord_client.model.action as AccordAction
import accord_client.model.data as AccordData
from accord_client import DataBuilder, SignalWaiter, protocol, settings
from accord_client.member import MemberController
from accord_client.model.action import ActionEncoder, ActionType

member = MemberController()


class ClientController(QObject):
    _instance = None

    emitDisconnected = pyqtSignal()
    emitReceiveCtrlMsg = pyqtSignal(str, str)
    emitUpdateMembersList = pyqtSignal(list)
    emitAcceptEnter = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.promise = None

        self._socket = QTcpSocket()
        self._socket.readyRead.connect(self.receive)
        self._socket.disconnected.connect(self.disconnected)

        self.protocolData = protocol.ProtocolData(bytearray())
        self.serverData = AccordData.ServerData()

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = QObject.__new__(cls, *args, **kw)
        return cls._instance

    def init(self):
        self.protocolData = protocol.ProtocolData(bytearray())
        self.serverData = AccordData.ServerData()

    def connect(self):
        [host, port] = settings.get_value("AccordServer", ["host", "port"])
        port = int(port)

        if self._socket.state() == QAbstractSocket.SocketState.ConnectedState:
            return

        print(f"[ServerController]: Try Connect {host}:{port}")

        self._socket.setSocketOption(QAbstractSocket.SocketOption.KeepAliveOption, 1)
        self._socket.connectToHost(QHostAddress(host), port)
        self.protocolData.readyConsume.connect(self.consume)

    def disconnected(self):
        print("[Accord]: Close Connection")
        self.init()
        self.emitDisconnected.emit()

    def receive(self):
        print("[Accord]: Client<<Server")
        if self.protocolData.consumed:
            chunk = self.protocolData.chunk
            self.protocolData = protocol.ProtocolData(chunk)
            self.protocolData.readyConsume.connect(self.consume)

        self.protocolData.onData(self._socket.readAll())  # type: ignore

    def leave(self):
        # print(self._socket.state())
        if self.serverData.hash == "":
            return
        self.request(ActionType.LEAVE)
        self._socket.disconnectFromHost()

    def enter(self, data: AccordData.ServerData):
        self.serverData = data
        self.promise = SignalWaiter(self._socket.connected, self.connect)  # type: ignore
        self.promise.then(lambda: self.request(ActionType.ENTER))

    def consume(self, header: protocol.ProtocolHeader, body: bytes):
        decode_body = body.decode("utf8")
        match header.Action:
            case ActionType.ACCEPT:
                actionData: AccordAction.ActionAccept = json.loads(
                    decode_body, object_hook=DataBuilder.accept
                )
                match actionData.action:
                    case ActionType.ENTER:
                        self.emitAcceptEnter.emit()
                    case _:
                        self.emitReceiveCtrlMsg.emit(decode_body, header.Action.value)

            case ActionType.UPDATE_MEMBERS:
                memberList = json.loads(
                    decode_body, object_hook=DataBuilder.update_members_list
                )
                print(memberList)
                self.emitUpdateMembersList.emit(memberList)

            case _:
                self.emitReceiveCtrlMsg.emit(decode_body, header.Action.value)
        print(decode_body, header.Action)

    def request(self, action: ActionType):
        body = b""
        content = ""
        match action:
            case ActionType.ENTER:
                content = json.dumps(
                    AccordAction.ActionEnter(
                        serverHash=self.serverData.hash,
                        memberHash=member.hash,
                        avatar=member.avatar,
                        name=member.name,
                    ),
                    cls=ActionEncoder,
                    ensure_ascii=False,
                )
            case ActionType.LEAVE:
                content = "离开服务器"

        body = content.encode("utf8")
        header = protocol.ProtocolHeader(
            Action=action,
            ContentEncoding=protocol.ProtocolEncoding.UTF8,
            ContentLength=len(body),
            ContentMime="application/json",
        )
        headerBuffer = json.dumps(header, cls=protocol.ProtocolHeaderEncoder).encode(
            "utf-8"
        )

        fixedLength = len(headerBuffer).to_bytes(4, sys.byteorder, signed=False)
        self._socket.write(fixedLength + headerBuffer + body)
