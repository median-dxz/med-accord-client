from dataclasses import dataclass, field


@dataclass
class ServerData:
    hash: str = field(default="")
    showName: str = field(default="")
    actualName: str = field(default="")
    icon: str = field(default="")


@dataclass
class MemberData:
    name: str = field(default="")
    avatar: str = field(default="")


