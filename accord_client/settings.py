import os
import typing

from PyQt6.QtCore import QSettings

from accord_client import baseDir

configMain = QSettings(os.path.join(baseDir, "config", "global.ini"), QSettings.Format.IniFormat)

def get_value(group: str, keys: list[str]):
    configMain.beginGroup(group)
    ret = []
    for key in keys:
        ret.append(configMain.value(key))
    configMain.endGroup()
    return ret

def set_value(group: str, entities: list[tuple[str, typing.Any]]):
    configMain.beginGroup(group)
    for key, value in entities:
        configMain.setValue(key, value)
    configMain.endGroup()

def init_settings():
    config_main = configMain
    config_main.beginGroup("ListService")

    if not config_main.contains("host"):
        config_main.setValue("host", "127.0.0.1")
    if not config_main.contains("port"):
        config_main.setValue("port", 4545)

    config_main.endGroup()

    config_main.beginGroup("AccordServer")

    if not config_main.contains("host"):
        config_main.setValue("host", "127.0.0.1")
    if not config_main.contains("port"):
        config_main.setValue("port", 9980)

    config_main.endGroup()

    config_main.beginGroup("UserInfo")

    if not config_main.contains("hash"):
        config_main.setValue("hash", "")
    if not config_main.contains("name"):
        config_main.setValue("name", "Accord萌新")
    if not config_main.contains("avatar"):
        config_main.setValue("avatar", "")

    config_main.endGroup()

init_settings()