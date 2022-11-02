from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QGridLayout, QLabel, QSizePolicy, QTextBrowser

from accord_client.widget.AvatarLabel import AvatarLabel


class Message(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super(Message, self).__init__(parent=parent)
        self.grid = QGridLayout(self)
        self.setLayout(self.grid)
        self.lab_username = QLabel("it's a username", self)
        self.lab_time = QLabel("it's a time", self)
        self.lab_avatar = AvatarLabel(self)
        self.text_content = QTextBrowser(self)
        self.grid.addWidget(self.lab_username, 0, 1)
        self.grid.addWidget(self.lab_time, 1, 1)
        self.grid.addWidget(self.lab_avatar, 0, 0, 2, 1)
        self.grid.addWidget(
            self.text_content,
            2,
            0,
            1,
            2,
        )
        self.setStyleSheet(
            """
            background-color: #ffffff;
        """
        )
        sizePolicy = self.sizePolicy()
        sizePolicy.setVerticalPolicy(QSizePolicy.Policy.Minimum)
        self.setSizePolicy(sizePolicy)
