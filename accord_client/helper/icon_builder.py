import base64
import binascii
import os

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap

from accord_client import IconsMap, baseDir


def getImageQIcon(path, scaled=[256, 256]) -> QIcon:
    filePath = os.path.join(baseDir, "assets", path)
    pix = QPixmap(filePath)
    icon = QIcon(pix.scaled(QSize(scaled[0], scaled[1])))
    return icon


def getBase64QIcon(data: str, scaled=[32, 32]) -> QIcon:
    try:
        byteData = base64.b64decode(data)
    except binascii.Error:
        byteData = b''
    pix = QPixmap()
    pix.loadFromData(byteData)  # type: ignore
    if (pix.isNull()):
        return getImageQIcon(IconsMap.server_default.value, [32, 32])
    else:
        icon = QIcon(pix.scaled(QSize(scaled[0], scaled[1])))
        return icon