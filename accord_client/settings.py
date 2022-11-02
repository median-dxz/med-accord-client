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
