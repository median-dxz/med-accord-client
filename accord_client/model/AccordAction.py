from dataclasses import dataclass, field
from enum import Enum
import json


class ActionType(Enum):
    TIMEOUT = "timeout"
    ENTER = "enter"
    LEAVE = "leave"


@dataclass
class ActionEnter:
    serverHash: str = field(default="")
    memberHash: str = field(default="")
    avatar: str = field(default="")
    name: str = field(default="")


class AccordActionEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ActionEnter):
            return {
                "serverHash": obj.serverHash,
                "memberHash": obj.memberHash,
                "avatar": obj.avatar,
                "name": obj.name,
            }
        return json.JSONEncoder.default(self, obj)