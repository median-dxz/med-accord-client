import os

from . import settings
from .helper import DataBuilder, PixmapBuilder
from .helper.SignalWaiter import SignalWaiter

__version__ = "0.0.1"
__appname__ = "Accord"
__comment__ = "Accord Client for Windows Desktop"
__domain__ = "xyz.median"
__desktopid__ = "xyz.median.accord.client"
__appid__ = "Accord-Client"

__author__ = "Median-dxz"
__licence__ = "GNU General Public License v3.0"

baseDir = os.path.dirname(__file__)


class Icons:
    LOGO = "icon.png"
    SERVER = "server_default.svg"
    AVATAR = "account_default.svg"
