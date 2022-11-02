import requests

from accord_client import settings


def getServerList():
    [host, port] = settings.getValue("ListService", ["host", "port"])
    res = requests.get(f"http://{host}:{port}/", timeout=1)

    if res.status_code != 200:
        raise Exception(f"服务器错误: {res.status_code}")

    result: list[dict] = res.json()
    return result


def requireHash():
    [host, port] = settings.getValue("ListService", ["host", "port"])

    res = requests.get(f"http://{host}:{port}/hash", timeout=1)

    if res.status_code != 200:
        raise Exception(f"服务器错误: {res.status_code}")

    result: dict[str, str] = res.json()

    settings.setValue("UserInfo", [("hash", result.get("hash"))])
