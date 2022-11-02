from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QSizePolicy, QWidget


class Message(QWidget):
    def __init__(self, parent) -> None:
        super(Message, self).__init__(parent=parent)
        self.grid = QGridLayout(self)
        self.setLayout(self.grid)
        self.grid.addWidget(QLabel("it's a username", self), 0, 1)
        self.grid.addWidget(QLabel("it's a time", self), 1, 1)
        self.grid.addWidget(QLabel("it's a avatar", self), 0, 0, 2, 1)
        self.grid.addWidget(
            QLabel(
                """it's a message
        wwwww
        wwww
        www
        asdf
        www
        www
        asdf
        asdf""",
                self,
            ),
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
