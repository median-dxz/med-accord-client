import base64
import binascii
import os

from PyQt6.QtCore import QSize, Qt, QFileInfo
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QWidget

from accord_client import baseDir


def fromPath(path: str, scaled=None) -> QPixmap:
    if scaled is None:
        scaled = [256, 256]
    filePath = os.path.join(baseDir, "assets", path)
    pix = QPixmap(filePath)
    if pix.isNull():
        pix = QPixmap(path)
    if pix.isNull():
        raise TypeError(f"can't load pixmap from path: {path}")
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


def selectImageFile(parent: QWidget):
    file_name, _ = QFileDialog.getOpenFileName(
        parent,
        "选择图片",
        os.path.join(
            os.environ["userprofile"] if os.getenv("userprofile") else os.getcwd(),
            "pictures",
        ),
        "图片文件 (*.png *.jpg *.svg)",
    )
    file_pix = QPixmap(file_name)
    if file_pix.isNull():
        raise FileNotFoundError(f"空文件: {file_name}")

    file_info = QFileInfo(file_name)

    return file_name, file_pix, file_info.size()
