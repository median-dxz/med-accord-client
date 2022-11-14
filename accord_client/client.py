import json
import sys
import typing
from datetime import datetime

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
    emitReceiveMessages = pyqtSignal(list)
    emitAcceptEnter = pyqtSignal()
    emitOnUploadFile = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.promise = None
        self._online = False

        self._socket = QTcpSocket()
        self._socket.readyRead.connect(self.receive)
        self._socket.connected.connect(self.connected)
        self._socket.disconnected.connect(self.disconnected)

        self.init()

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = QObject.__new__(cls, *args, **kw)
        return cls._instance

    def init(self):
        self.protocolData = protocol.ProtocolData()
        self.protocolData.readyConsume.connect(self.consume)

        self.serverData = AccordData.ServerData()

    @property
    def online(self):
        return self._online

    def connect(self):
        [host, port] = settings.get_value("AccordServer", ["host", "port"])
        port = int(port)

        if self._socket.state() == QAbstractSocket.SocketState.ConnectedState:
            return

        print(f"[ServerController]: Try Connect {host}:{port}")

        self._socket.setSocketOption(QAbstractSocket.SocketOption.KeepAliveOption, 1)
        self._socket.connectToHost(QHostAddress(host), port)

    def connected(self):
        self._online = True

    def disconnected(self):
        print("[Accord]: Close Connection")
        self.init()
        self.emitDisconnected.emit()
        self._online = False

    def receive(self):
        print("[Accord]: Client<<Server")

        self.protocolData.onData(self._socket.readAll())  # type: ignore

        while self.protocolData.consumed:
            self.protocolData.init()
            self.protocolData.onData()

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

    def send(self, messageText: str):
        self.request(
            ActionType.SEND_MESSAGE, messageText, type=AccordData.MessageType.TEXT
        )

    def sendImage(self, imageData: str):
        self.request(
            ActionType.SEND_MESSAGE,
            imageData,
            type=AccordData.MessageType.IMAGE,
        )

    def updateMemberList(self):
        self.request(ActionType.UPDATE_MEMBERS)

    def setMemberInfo(self):
        self.request(ActionType.SET_MEMBER)

    def getHistoryMessage(
        self, timestamp: typing.Optional[datetime] = None, max_limit=30
    ):
        if timestamp is None:
            timestamp = datetime.now()
        self.request(ActionType.HISTORY_MESSAGES, limit=max_limit, timestamp=timestamp)

    def consume(self, header: protocol.ProtocolHeader, body: bytes):
        decode_body = body.decode("utf8")
        print(header.Action, len(decode_body))
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
                self.emitUpdateMembersList.emit(memberList)

            case ActionType.RECEIVE_MESSAGES:
                message = json.loads(decode_body, object_hook=DataBuilder.message)
                self.emitReceiveMessages.emit(message)

            case _:
                self.emitReceiveCtrlMsg.emit(decode_body, header.Action.value)

    def request(self, action: ActionType, *body_arg, **kw_args):
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
            case ActionType.SEND_MESSAGE:
                content = json.dumps(
                    AccordData.MessageData(
                        avatar=member.avatar,
                        name=member.name,
                        content=body_arg[0],
                        type=kw_args["type"],
                    ),
                    cls=AccordData.MessageEncoder,
                    ensure_ascii=False,
                )
            case ActionType.UPDATE_MEMBERS:
                content = "更新用户列表"
            case ActionType.SET_MEMBER:
                content = json.dumps(
                    AccordAction.ActionSetMember(
                        avatar=member.avatar,
                        name=member.name,
                    ),
                    cls=ActionEncoder,
                    ensure_ascii=False,
                )
            case ActionType.HISTORY_MESSAGES:
                content = json.dumps(
                    AccordAction.ActionHistoryMessages(
                        limit=kw_args["limit"], timestamp=kw_args["timestamp"]
                    ),
                    cls=AccordAction.ActionEncoder,
                    ensure_ascii=False,
                )

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
