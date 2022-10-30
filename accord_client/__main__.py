import ctypes
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox

import accord_client
from accord_client.provider.single_instance import SingleInstance
import accord_client.helper.icon_builder as IconBuilder
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

        dialog = QMessageBox(title="启动失败", text="Accord客户端实例已经运行", icon=QMessageBox.Icon.Warning, parent=window)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

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
    app.setWindowIcon(QIcon(IconBuilder.getQPixmapFromPath(accord_client.IconsMap.logo.value)))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(accord_client.__appid__)


if __name__ == "__main__":
    main()
