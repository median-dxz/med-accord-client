from collections import namedtuple
from typing import Any
import requests

from accord_client import globalSettings


def getServerList():
    globalSettings.beginGroup("ListService")
    [host, port] = [globalSettings.value("host"), globalSettings.value("port")]
    globalSettings.endGroup()
    res = requests.get(f"http://{host}:{port}/", timeout=1)

    if (res.status_code != 200):
        raise Exception(f"服务器错误: {res.status_code}")

    result: list[dict] = res.json()
    return result


def JoinServer():
    pass


def SignInServer():
    pass


def SignOutServer():
    pass
