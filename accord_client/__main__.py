import ctypes
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox

import accord_client as accord
from accord_client import PixmapBuilder, settings
from accord_client.single_instance import SingleInstance
from accord_client.window.main_window import AccordMainWindow


def main():
    instance = SingleInstance(accord.__appid__)
    app = QApplication([])
    init_app(app)
    init_settings()

    window = AccordMainWindow(app)
    window.show()
    app.setActiveWindow(window)

    if instance.isRunning():
        print("An instance is running now!")

        dialog = QMessageBox(QMessageBox.Icon.Warning, "启动失败", "Accord客户端实例已经运行", parent=window)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        dialog.exec()
        app.exit(0)
        # app.exec()
        sys.exit(0)
    else:
        result = app.exec()
        instance.close()
        sys.exit(result)


def init_app(app: QApplication):
    app.setApplicationName(accord.__appname__)
    app.setApplicationVersion(accord.__version__)
    app.setDesktopFileName(accord.__desktopid__)
    app.setOrganizationDomain(accord.__domain__)
    print("baseDir: " + accord.baseDir)
    app.setWindowIcon(QIcon(PixmapBuilder.getQPixmapFromPath(accord.Icons.LOGO)))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(accord.__appid__)


def init_settings():
    configMain = settings.configMain
    configMain.beginGroup("ListService")

    if not configMain.contains("host"):
        configMain.setValue("host", "127.0.0.1")
    if not configMain.contains("port"):
        configMain.setValue("port", 4545)

    configMain.endGroup()

    configMain.beginGroup("AccordServer")

    if not configMain.contains("host"):
        configMain.setValue("host", "127.0.0.1")
    if not configMain.contains("port"):
        configMain.setValue("port", 9980)

    configMain.endGroup()

    configMain.beginGroup("UserInfo")

    if not configMain.contains("hash"):
        configMain.setValue("hash", "")
    if not configMain.contains("name"):
        configMain.setValue("name", "Accord萌新")
    if not configMain.contains("avatar"):
        configMain.setValue("avatar", "")

    configMain.endGroup()


if __name__ == "__main__":
    main()
