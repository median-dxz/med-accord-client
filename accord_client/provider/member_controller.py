from PyQt6.QtCore import QObject, pyqtSignal

import accord_client as Accord
import accord_client.helper.icon_builder as IconBuilder
from accord_client.provider import network_service as NetworkService
import typing


class MemberController(QObject):
    _instance = None

    emitUpdateHash = pyqtSignal("QString")

    def __init__(self) -> None:
        super().__init__()
        self.name = None
        self.avatar = None
        [self._hash] = Accord.getValue("UserInfo", ["hash"])

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

    def getName(self):
        if self.name is None:
            return ""
        else:
            return self.name

    def getAvatar(self):
        if self.avatar is None:
            return ""
        else:
            return self.avatar

    def getAvatarPixmap(self):
        return IconBuilder.getQPixmapFromBase64(self.getAvatar(), Accord.IconsMap.avatar_default.value)
