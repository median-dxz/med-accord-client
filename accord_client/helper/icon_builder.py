import base64
import binascii
import os

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap

from accord_client import baseDir


def getQPixmapFromPath(path, scaled=[256, 256]) -> QPixmap:
    filePath = os.path.join(baseDir, "assets", path)
    pix = QPixmap(filePath)
    pix = pix.scaled(QSize(scaled[0], scaled[1]))
    return pix


def getQPixmapFromBase64(data: str, default: str, scaled=[24, 24]) -> QPixmap:
    try:
        byteData = base64.b64decode(data)
    except binascii.Error:
        byteData = b''
    pix = QPixmap()
    pix.loadFromData(byteData)  # type: ignore
    if (pix.isNull()):
        return getQPixmapFromPath(default, scaled)
    else:
        return pix.scaled(QSize(scaled[0], scaled[1]))
