import ctypes
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

import accord_client
from accord_client.provider.single_instance import SingleInstance
from accord_client.helper.icon_builder import getImageQIcon
from accord_client.window.main_window import AccordMainWindow


def main():
    instance = SingleInstance(accord_client.__appid__)
    app = QApplication([])
    init_app(app)

    window = AccordMainWindow(app)
    window.show()
    app.setActiveWindow(window)

    if instance.isRunning():
        print("An instance is running now!")
        dialog = QMessageBox(window)

        dialog.setWindowTitle("启动失败")
        dialog.setText("Accord客户端实例已经运行")
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.setIcon(QMessageBox.Icon.Warning)

        dialog.exec()
        app.exit(0)
        sys.exit(0)
    else:
        result = app.exec()
        instance.close()
        sys.exit(result)


def init_app(app: QApplication):
    app.setApplicationName(accord_client.__appname__)
    app.setApplicationVersion(accord_client.__version__)
    app.setDesktopFileName(accord_client.__desktopid__)
    app.setOrganizationDomain(accord_client.__domain__)
    print("baseDir: " + accord_client.baseDir)
    app.setWindowIcon(getImageQIcon(accord_client.IconsMap.logo.value))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(accord_client.__appid__)


if __name__ == "__main__":
    main()
