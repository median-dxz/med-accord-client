from dataclasses import dataclass
from enum import Enum
import typing

from PyQt6.QtCore import QAbstractListModel, QModelIndex
from PyQt6.QtCore import Qt

from accord_client.helper import icon_builder as IconBuilder

@dataclass
class ServerData:
    hash: str
    showName: str
    actualName: str
    icon: str

class ServerAction(Enum):
    Accept = 1
    Enter = 2
    Leave = 3
    

class ServerDataModel(QAbstractListModel):
    serverList: list[ServerData] = []

    def __init__(self) -> None:
        super().__init__()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        value = self.serverList[index.row()]
        match role:
            case Qt.ItemDataRole.DisplayRole:
                return value.showName
            case Qt.ItemDataRole.ToolTipRole:
                return f"{value.showName} - {value.actualName}#{value.hash}"
            case Qt.ItemDataRole.DecorationRole:
                return IconBuilder.getBase64QIcon(value.icon)
            case Qt.ItemDataRole.UserRole:
                return value
            case _:
                return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.serverList)
    
    def setServerData(self, serverList:list[ServerData]):
        self.serverList = serverList