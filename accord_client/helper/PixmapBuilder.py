import base64
import binascii
import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap

from accord_client import baseDir


def fromPath(path: str, scaled=None) -> QPixmap:
    if scaled is None:
        scaled = [256, 256]
    filePath = os.path.join(baseDir, "assets", path)
    pix = QPixmap(filePath)
    return scale(pix=pix, scaled=scaled)


def toBase64fromPath(path: str) -> str:
    with open(path, "rb") as f:
        byteData = base64.encodebytes(f.read())

    return byteData.decode("utf8")


def fromBase64(data: str, default: str, scaled=None) -> QPixmap:
    if scaled is None:
        scaled = [24, 24]
    try:
        byteData = base64.b64decode(data)
    except binascii.Error:
        byteData = b""
    except TypeError:
        byteData = b""
    pix = QPixmap()
    pix.loadFromData(byteData)  # type: ignore
    if pix.isNull():
        pix = QPixmap(os.path.join(baseDir, "assets", default))

    return scale(pix=pix, scaled=scaled)


def scale(pix: QPixmap, scaled) -> QPixmap:

    if isinstance(scaled, list):
        to_scale = QSize(scaled[0], scaled[1])
    else:
        to_scale = QSize(scaled)

    return pix.scaled(
        to_scale,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
