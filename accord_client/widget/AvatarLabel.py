
from PyQt6.QtCore import QFileInfo, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QPushButton

from accord_client import IconsMap


class RoundButton(QPushButton):

    radius = 24
    avatar: QPixmap = QPixmap(IconsMap.server_default.value)

    def __init__(self, parent) -> None:
        super(RoundButton, self).__init__(parent=parent)
        size = QSize(self.radius * 2, self.radius * 2)
        self.setFixedSize(size)
        self.setStyleSheet(f"""
RoundButton {{
    border-radius: 9px;
    color: white;
    background: #f44336;
}}

RoundButton:hover {{
    color: white;
    background: #d5d5d5; 
}}

RoundButton:pressed {{
    border-radius: 9px;
    background: #f2f2f2;
}}
        """)

    def setAvatar(self):
        pass

    def getAvatar(self):
        pass
