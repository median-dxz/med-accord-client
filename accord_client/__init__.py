__version__ = '0.0.1'
__appname__ = 'Accord'
__comment__ = 'Accord Client for Windows Desktop'
__domain__ = 'xyz.median'
__desktopid__ = 'xyz.median.accord.client'
__appid__ = 'Accord-Client'

__author__ = 'Median-dxz'
__licence__ = 'GNU General Public License v3.0'

import os
from enum import Enum
import typing

from PyQt6.QtCore import QSettings

baseDir = os.path.dirname(__file__)


class IconsMap(Enum):
    logo = os.path.join(baseDir, "assets", "icon.png")
    server_default = os.path.join(baseDir, "assets", "server_default.svg")
    avatar_default = os.path.join(baseDir, "assets", "account_default.svg")


globalSettings = QSettings(os.path.join(baseDir, "config", "global.ini"), QSettings.Format.IniFormat)

globalSettings.beginGroup("ListService")

if (not globalSettings.contains("host")):
    globalSettings.setValue("host", "127.0.0.1")

if (not globalSettings.contains("port")):
    globalSettings.setValue("port", 4545)

globalSettings.endGroup()

globalSettings.beginGroup("AccordServer")

if (not globalSettings.contains("host")):
    globalSettings.setValue("host", "127.0.0.1")

if (not globalSettings.contains("port")):
    globalSettings.setValue("port", 9980)

globalSettings.endGroup()

globalSettings.beginGroup("UserInfo")

if (not globalSettings.contains("hash")):
    globalSettings.setValue("hash", "")

globalSettings.endGroup()


def getValue(group: str, keys: list[str]):
    globalSettings.beginGroup(group)
    ret = []
    for key in keys:
        ret.append(globalSettings.value(key))
    globalSettings.endGroup()
    return ret


def setValue(group: str, entities: list[tuple[str, typing.Any]]):
    globalSettings.beginGroup(group)
    for k, v in entities:
        globalSettings.setValue(k, v)
    globalSettings.endGroup()