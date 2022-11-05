from datetime import datetime

import accord_client.model.data as AccordData
from accord_client.model import action
from accord_client.model.action import ActionType


def server(data: dict):
    return AccordData.ServerData(
        hash=str(data["hash"]),
        actualName=str(data["actualName"]),
        icon=str(data["icon"]),
        showName=str(data["showName"]),
    )


def update_members_list(data: dict):
    return AccordData.MemberData(name=str(data["name"]), avatar=str(data["avatar"]))


def accept(data: dict):
    return action.ActionAccept(msg=str(data["msg"]), action=ActionType(data["action"]))


def message(data: dict):
    return AccordData.MessageData(
        index=int(data["index"]),
        name=str(data["name"]),
        avatar=str(data["avatar"]),
        content=str(data["content"]),
        date=datetime.fromtimestamp(data["date"]),
        type=AccordData.MessageType(data["type"]),
    )