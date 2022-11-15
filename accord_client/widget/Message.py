import base64
from hashlib import md5
from datetime import datetime

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QGridLayout, QLabel, QSizePolicy, QTextBrowser

from accord_client import Icons, PixmapBuilder, baseDir
from accord_client import data_cache as DataCache
from accord_client.model.data import MessageData, MessageType
from accord_client.widget.AvatarLabel import AvatarLabel

StyleTextContent = """
QTextBrowser{
    border: none;
}

QTextBrowser::hover{
    background-color: #fafafa
}
"""


class Message(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super(Message, self).__init__(parent=parent)
        self.grid = QGridLayout(self)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 8)
        self.setLayout(self.grid)

        self.lab_username = QLabel(self)
        self.lab_time = QLabel(self)
        self.lab_avatar = AvatarLabel(self)
        self.text_content = QTextBrowser(self)

        self.lab_username.setStyleSheet("padding-left: 10px;")
        self.lab_time.setStyleSheet("padding-left: 10px;")
        self.text_content.setStyleSheet(StyleTextContent)

        self.grid.addWidget(self.lab_username, 0, 1)
        self.grid.addWidget(self.lab_time, 1, 1)
        self.grid.addWidget(self.lab_avatar, 0, 0, 2, 1)
        self.grid.addWidget(self.text_content, 2, 1, 1, 1)

        self.setStyleSheet("background-color: #ffffff;")

        sizePolicy = self.sizePolicy()
        sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Maximum)
        self.setSizePolicy(sizePolicy)

    def setMessage(self, message: MessageData):
        document = self.text_content.document()
        if message.type == MessageType.TEXT:
            document.setMarkdown(message.content)
        elif message.type == MessageType.IMAGE:
            image_data = message.content.encode("utf-8")
            image_path = DataCache.get_from_cache(image_data)
            document.setHtml(f"<img src='{image_path}' width={self.width()-64}/>")
        text_height = int(document.size().height())
        self.text_content.setFixedHeight(text_height)
        self.lab_avatar.setAvatar(
            PixmapBuilder.fromBase64(message.avatar, Icons.AVATAR, [36, 36])
        )
        self.lab_username.setText(message.name)
        self.lab_time.setText(message.date.strftime("%m/%d %H:%M:%S"))
