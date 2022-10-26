from PyQt6.QtCore import pyqtSignal

from accord_client.model.AccordServer import ServerData

tcpConnection = None


class ServerController:
    _instance = None

    ServerEventAccept = pyqtSignal()

    def __init__(self):
        pass

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def enter(self, server: ServerData):
        pass