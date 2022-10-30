from PyQt6.QtCore import QObject, pyqtSignal

import accord_client as Accord
import accord_client.helper.icon_builder as IconBuilder
from accord_client.model.AccordServer import MemberData
from accord_client.provider import network_service as NetworkService
import typing


class MemberController(QObject):
    _instance = None

    emitUpdateHash = pyqtSignal("QString")

    def __init__(self) -> None:
        super().__init__()
        self._hash = ""
        [self._hash, name, avatar] = Accord.getValue("UserInfo", ["hash", "name", "avatar"])
        self.data = MemberData(name=name, avatar=avatar)

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = QObject.__new__(cls, *args, **kw)
        return cls._instance

    def updateMemberHash(self):
        NetworkService.requireHash()
        [self._hash] = Accord.getValue("UserInfo", ["hash"])
        self.emitUpdateHash.emit(f"#{self._hash}")

    def getMemberHash(self) -> str:
        return self._hash

    def getName(self) -> str:
        return self.data.name

    def getAvatar(self) -> str:
        return self.data.avatar

    def setAvatar(self, avatar: str):
        self.data.avatar = avatar

    def setName(self, name: str):
        self.data.name = name

    def getAvatarPixmap(self):
        return IconBuilder.getQPixmapFromBase64(self.getAvatar(), Accord.IconsMap.avatar_default.value, [48, 48])
