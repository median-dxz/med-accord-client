from dataclasses import dataclass, field
from enum import Enum
import typing

from PyQt6.QtCore import QAbstractListModel, QModelIndex
from PyQt6.QtCore import Qt

import accord_client as Accord

from accord_client.helper import icon_builder as IconBuilder
from accord_client.model import AccordAction

@dataclass
class ServerData:
    hash: str = field(default="")
    showName: str = field(default="")
    actualName: str = field(default="")
    icon: str = field(default="")

class ProtocolDataEncoding(Enum):
    UTF8 = "utf8"
    BINARY = "binary"
    
@dataclass
class ProtocolDataHeader:
    ContentLength: int
    ContentMime: str
    ContentEncoding: ProtocolDataEncoding
    Action: AccordAction.ActionType


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
                return IconBuilder.getQPixmapFromBase64(value.icon, Accord.IconsMap.server_default.value)
            case Qt.ItemDataRole.UserRole:
                return value
            case _:
                return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.serverList)
    
    def setServerData(self, serverList:list[ServerData]):
        self.serverList = serverList
