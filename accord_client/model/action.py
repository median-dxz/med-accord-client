import json
from dataclasses import dataclass, field
from enum import Enum


class ActionType(Enum):
    TIMEOUT = "timeout"
    ENTER = "enter"
    LEAVE = "leave"
    ACCEPT = "accept"
    REFUSE = "refuse"
    UPDATE_MEMBERS = "updateMemberList"


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


class ActionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ActionEnter):
            return {
                "serverHash": obj.serverHash,
                "memberHash": obj.memberHash,
                "avatar": obj.avatar,
                "name": obj.name,
            }
        return json.JSONEncoder.default(self, obj)
