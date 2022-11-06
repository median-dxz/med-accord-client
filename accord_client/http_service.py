import requests

from accord_client import settings


def get_server_list():
    [host, port] = settings.get_value("ListService", ["host", "port"])
    res = requests.get(f"http://{host}:{port}/", timeout=1)

    if res.status_code != 200:
        raise Exception(f"服务器错误: {res.status_code}")

    result: list[dict] = res.json()
    return result


def require_hash():
    [host, port] = settings.get_value("ListService", ["host", "port"])

    res = requests.get(f"http://{host}:{port}/hash", timeout=1)

    if res.status_code != 200:
        raise Exception(f"服务器错误: {res.status_code}")

    result: dict[str, str] = res.json()

    settings.set_value("UserInfo", [("hash", result.get("hash"))])


def create_server(displayName: str, actualName: str, icon: str):
    [host, port] = settings.get_value("ListService", ["host", "port"])

    res = requests.post(
        f"http://{host}:{port}/create",
        json={"displayName": displayName, "actualName": actualName, "icon": icon},
        timeout=1,
    )

    if res.status_code != 200:
        raise Exception(f"服务器错误: {res.status_code}")

    result: dict[str, str] = res.json()

    return result