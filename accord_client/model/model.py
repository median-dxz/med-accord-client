import typing
from dataclasses import dataclass, field

from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt

from accord_client import Icons, PixmapBuilder
from accord_client.model import data as AccordData


class ServerDataModel(QAbstractListModel):
    serverList: list[AccordData.ServerData] = []

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
                return PixmapBuilder.fromBase64(value.icon, Icons.SERVER)
            case Qt.ItemDataRole.UserRole:
                return value
            case _:
                return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.serverList)

    def setServerData(self, serverList: list[AccordData.ServerData]):
        self.serverList = serverList


class MembersListModel(QAbstractListModel):
    memberList: list[AccordData.MemberData] = []

    def __init__(self) -> None:
        super().__init__()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        value = self.memberList[index.row()]
        match role:
            case Qt.ItemDataRole.DisplayRole:

                return value.name
            case Qt.ItemDataRole.ToolTipRole:
                return f"{value.name}"
            case Qt.ItemDataRole.DecorationRole:
                return PixmapBuilder.fromBase64(value.avatar, Icons.AVATAR, [24, 24])
            case Qt.ItemDataRole.UserRole:
                return value
            case _:
                return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.memberList)

    def setMembersList(self, memberList: list[AccordData.MemberData]):
        self.memberList = memberList
