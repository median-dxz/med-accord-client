from PyQt6.QtCore import QObject, pyqtSignal

from accord_client import Icons, PixmapBuilder
from accord_client import http_service as HttpService
from accord_client import settings
from accord_client.model import data as AccordData


class MemberController(QObject):
    _instance = None

    emitUpdateHash = pyqtSignal("QString")
    emitUpdateInfo = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._hash = ""
        [self._hash, _name, _avatar] = settings.get_value(
            "UserInfo", ["hash", "name", "avatar"]
        )
        self.data = AccordData.MemberData(name=_name, avatar=_avatar)

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = QObject.__new__(cls, *args, **kw)
        return cls._instance

    def updateMemberHash(self):
        try:
            HttpService.require_hash()
            [self._hash] = settings.get_value("UserInfo", ["hash"])
            self.emitUpdateHash.emit(f"#{self._hash}")
        except TimeoutError:
            pass
        except Exception:
            pass

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def name(self) -> str:
        return self.data.name

    @property
    def avatar(self) -> str:
        return self.data.avatar

    @avatar.setter
    def avatar(self, avatar: str):
        self.data.avatar = avatar
        settings.set_value("UserInfo", [("avatar", avatar)])
        self.emitUpdateInfo.emit()

    @name.setter
    def name(self, name: str):
        self.data.name = name
        settings.set_value("UserInfo", [("name", name)])
        self.emitUpdateInfo.emit()

    def getAvatarPixmap(self):
        return PixmapBuilder.fromBase64(self.avatar, Icons.AVATAR, [36, 36])
