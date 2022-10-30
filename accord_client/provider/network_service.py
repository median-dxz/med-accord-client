import requests

import accord_client as Accord


def getServerList():
    [host, port] = Accord.getValue("ListService", ["host", "port"])
    res = requests.get(f"http://{host}:{port}/", timeout=1)

    if (res.status_code != 200):
        raise Exception(f"服务器错误: {res.status_code}")

    result: list[dict] = res.json()
    return result


def requireHash():
    [host, port] = Accord.getValue("ListService", ["host", "port"])

    res = requests.get(f"http://{host}:{port}/hash", timeout=1)

    if (res.status_code != 200):
        raise Exception(f"服务器错误: {res.status_code}")

    result: dict[str, str] = res.json()

    Accord.setValue("UserInfo", [("hash", result.get("hash"))])
