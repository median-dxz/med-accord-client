import typing

from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QWidget

from accord_client.widget.AvatarLabel import AvatarLabel


class DialogCreateServer(QDialog):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.layout_form = QFormLayout(self)
        self.editDisplayName = QLineEdit(self)
        self.editActualName = QLineEdit(self)
        self.editIcon = AvatarLabel(self)

        self.layout_form.addRow("显示名称:", self.editDisplayName)
        self.layout_form.addRow("标识名称:", self.editActualName)
        self.layout_form.addRow("图标:", self.editIcon)

        self.setModal(True)
