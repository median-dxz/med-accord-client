from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPixmap
from PyQt6.QtWidgets import QLabel

from accord_client import Icons, PixmapBuilder

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

    doubleClicked = pyqtSignal()
    radius = 18
    avatar: QPixmap

    def __init__(self, parent) -> None:
        super(AvatarLabel, self).__init__(parent=parent)
        size = QSize(self.radius * 2, self.radius * 2)
        self.setFixedSize(size)
        self.setStyleSheet(StyleSheet)

    def setAvatar(self, pixmap: QPixmap):
        if not pixmap is None:
            self.avatar = PixmapBuilder.scale(pixmap, self.size())
        else:
            self.avatar = PixmapBuilder.fromPath(Icons.AVATAR, self.size())
        self.setPixmap(self.avatar)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.doubleClicked.emit()
        return super().mouseDoubleClickEvent(a0)
