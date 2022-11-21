from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QSizePolicy,
    QTextEdit,
    QAbstractScrollArea,
    QFileDialog,
)

from accord_client import Icons, PixmapBuilder
from accord_client import data_cache as DataCache
from accord_client.model.data import MessageData, MessageType
from accord_client.widget.AvatarLabel import AvatarLabel

StyleTextContent = """
QTextEdit{
    border: none;
}

QTextEdit::hover{
    background-color: #fafafa
}
"""


class Message(QtWidgets.QWidget):
    emitDoubleClickMessage = pyqtSignal()

    def __init__(self, parent) -> None:
        super(Message, self).__init__(parent=parent)
        self.grid = QGridLayout(self)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 8)
        self.setLayout(self.grid)

        self.lab_username = QLabel(self)
        self.lab_time = QLabel(self)
        self.lab_avatar = AvatarLabel(self)
        self.text_content = QTextEdit(self)

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

        self.text_content.setReadOnly(True)
        self.text_content.mouseDoubleClickEvent = self.editMouseDoubleClicked
        self.message = None

    def setMessage(self, message: MessageData):
        document = self.text_content.document()
        self.message = message
        if message.type == MessageType.TEXT:
            document.setMarkdown(message.content.decode("utf8"))
        elif message.type == MessageType.IMAGE:
            image_data = message.content
            image_path = DataCache.get_from_cache(image_data)
            document.setHtml(f"<img src='{image_path}' width={self.width()-64}/>")
        elif message.type == MessageType.FILE:
            document.setHtml(f"<p>[文件]</p>")
        text_height = int(document.size().height())
        self.text_content.setFixedHeight(text_height)
        self.lab_avatar.setAvatar(
            PixmapBuilder.fromBase64(message.avatar, Icons.AVATAR, [36, 36])
        )
        self.lab_username.setText(message.name)
        self.lab_time.setText(message.date.strftime("%m/%d %H:%M:%S"))

    def editMouseDoubleClicked(self, e):
        if not self.message is None and self.message.type != MessageType.TEXT:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "选择存储位置",
            )
            if file_name != "":
                with open(file_name, "wb") as f:
                    f.write(self.message.content)
        return QAbstractScrollArea.mouseDoubleClickEvent(self.text_content, e)
