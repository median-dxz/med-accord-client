from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QAbstractSocket, QHostAddress, QTcpSocket

from accord_client import globalSettings
from accord_client.model import AccordServer
from accord_client.provider import protocol_controller as ProtocolController


class ClientController(QObject):
    _instance = None

    serverData = None

    def __init__(self) -> None:
        super().__init__()

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = QObject.__new__(cls, *args, **kw)
        return cls._instance

    def connect(self):
        globalSettings.beginGroup("AccordServer")
        host = globalSettings.value("host")
        port = int(globalSettings.value("port"))
        globalSettings.endGroup()

        print(f"[ServerController]: Try Connect {host}:{port}")

        self._socket = QTcpSocket()

        self._socket.setSocketOption(QAbstractSocket.SocketOption.KeepAliveOption, 1)

        self._socket.connectToHost(QHostAddress(host), port)

        self._socket.readyRead.connect(self.receive)
        self._socket.disconnected.connect(self.disconnected)

        self.protocolData = ProtocolController.ProtocolData(bytearray())
        self.protocolData.readyConsume.connect(self.consume)

    def disconnected(self):
        print(f"[Accord]: Close Connection")

    def receive(self):
        print(f"[Accord]: Client<<Server")
        if self.protocolData.consumed:
            chunk = self.protocolData.chunk
            self.protocolData.readyConsume.disconnect(self.consume)
            self.protocolData = ProtocolController.ProtocolData(chunk)
            self.protocolData.readyConsume.connect(self.consume)

        self.protocolData.onData(self._socket.readAll())  # type: ignore

    def enter(self, server: AccordServer.ServerData):
        # self.disconnect()
        self.connect()
        # self._socket.writeData(b'{action:enter}')

    def consume(self, header: AccordServer.ProtocolDataHeader, body: bytes):
        print(body.decode(), header.Action)
