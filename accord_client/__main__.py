import argparse
import ctypes
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox

import accord_client as accord
from accord_client import PixmapBuilder, settings
from accord_client.single_instance import SingleInstance
from accord_client.window.main_window import AccordMainWindow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="turn on debug mode", action="store_true")
    args = parser.parse_args()

    instance = SingleInstance(accord.__appid__, args.debug)

    if args.debug:
        print("the application now on debug mode")

    app = QApplication([])
    init_app(app)

    window = AccordMainWindow(app)
    window.show()
    app.setActiveWindow(window)

    if instance.is_running():
        print("An instance is running now!")

        dialog = QMessageBox(
            QMessageBox.Icon.Warning, "启动失败", "Accord客户端实例已经运行", parent=window
        )
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
    app.setWindowIcon(QIcon(PixmapBuilder.fromPath(accord.Icons.LOGO)))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(accord.__appid__)

if __name__ == "__main__":
    main()
