import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass
class ServerData:
    hash: str = field(default="")
    showName: str = field(default="")
    actualName: str = field(default="")
    icon: str = field(default="")

    def __format__(self, __format_spec: str) -> str:
        return f"{self.showName} - {self.actualName}#{self.hash}"


@dataclass
class MemberData:
    name: str = field(default="")
    avatar: str = field(default="")


class MessageType(Enum):
    IMAGE = "image"
    FILE = "file"
    TEXT = "text"


@dataclass
class MessageData:
    index: int = field(default=-1)
    type: MessageType = field(default=MessageType.TEXT)
    avatar: str = field(default="")
    name: str = field(default="")
    date: datetime = field(default_factory=datetime.now)
    content: str = field(default="")


class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MessageData):
            return {
                "index": obj.index,
                "type": obj.type.value,
                "content": obj.content,
                "date": int(obj.date.timestamp()),
                "name": obj.name,
                "avatar": obj.avatar,
            }
        return json.JSONEncoder.default(self, obj)
