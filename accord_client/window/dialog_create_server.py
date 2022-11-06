import typing

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox

from accord_client import Icons, PixmapBuilder
from accord_client.widget.AvatarLabel import AvatarLabel


class DialogCreateServer(QDialog):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.layout_form = QtWidgets.QFormLayout(self)
        self.editDisplayName = QLineEdit(self)
        self.editActualName = QLineEdit(self)
        self.editIcon = AvatarLabel(self)
        self.buttonOk = QtWidgets.QPushButton("确认", self)

        self.layout_form.addRow("显示名称:", self.editDisplayName)
        self.layout_form.addRow("标识名称:", self.editActualName)
        self.layout_form.addRow("图标:", self.editIcon)

        self.layout_form.addWidget(self.buttonOk)

        self.buttonOk.clicked.connect(lambda: self.accept())
        self.editIcon.doubleClicked.connect(self.selectIcon)

        self.editIcon.setAvatar(PixmapBuilder.fromPath(Icons.SERVER, [24, 24]))
        self.icon_path = ""

        self.setModal(True)

    def accept(self) -> None:
        QMessageBox.information(self, "Accord", "服务器创建成功! 请重启Accord查看最新的服务器列表")
        return super().accept()

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        return super().closeEvent(e)

    def selectIcon(self):
        try:
            self.icon_path = PixmapBuilder.selectImageFile(self)
        except Exception:
            pass
