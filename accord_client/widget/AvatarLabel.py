from PyQt6.QtCore import QFileInfo, QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from accord_client import IconsMap
from accord_client.helper import icon_builder as IconBuilder

StyleSheet = f"""
AvatarLabel {{
    border-radius: 9px;
    background: #ffffff;
}}

AvatarLabel:hover {{
    background: #dbdee1;
}}
"""


class AvatarLabel(QLabel):

    radius = 18
    avatar: QPixmap

    def __init__(self, parent) -> None:
        super(AvatarLabel, self).__init__(parent=parent)
        size = QSize(self.radius * 2, self.radius * 2)
        self.setFixedSize(size)
        self.setStyleSheet(StyleSheet)

    def setAvatar(self, pixmap: QPixmap):
        if (not pixmap is None):
            self.avatar = pixmap
        else:
            self.avatar = IconBuilder.getQPixmapFromPath(IconsMap.avatar_default.value)
        self.avatar = self.avatar.scaled(self.size())
        self.setPixmap(self.avatar)