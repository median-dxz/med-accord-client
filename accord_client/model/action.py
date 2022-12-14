import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ActionType(Enum):
    TIMEOUT = "timeout"
    ENTER = "enter"
    LEAVE = "leave"
    ACCEPT = "accept"
    REFUSE = "refuse"
    UPDATE_MEMBERS = "updateMemberList"
    SET_MEMBER = "setMemberInfo"
    SEND_MESSAGE = "sendMessage"
    RECEIVE_MESSAGES = "receiveMessage"
    HISTORY_MESSAGES = "historyMessages"
    UNKNOWN = "unknown"


@dataclass
class ActionEnter:
    serverHash: str = field(default="")
    memberHash: str = field(default="")
    avatar: str = field(default="")
    name: str = field(default="")


@dataclass
class ActionAccept:
    action: ActionType
    msg: str = field(default="")


@dataclass
class ActionHistoryMessages:
    limit: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ActionSetMember:
    avatar: str = field(default="")
    name: str = field(default="")


class ActionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ActionEnter):
            return {
                "serverHash": obj.serverHash,
                "memberHash": obj.memberHash,
                "avatar": obj.avatar,
                "name": obj.name,
            }
        if isinstance(obj, ActionHistoryMessages):
            return {
                "limit": obj.limit,
                "timestamp": int(obj.timestamp.timestamp()),
            }
        if isinstance(obj, ActionSetMember):
            return {
                "avatar": obj.avatar,
                "name": obj.name,
            }
        return json.JSONEncoder.default(self, obj)
