import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtCore import Qt, QModelIndex

from requests.exceptions import Timeout

from accord_client import IconsMap, __appname__ as AppName
from accord_client.controller.server_controller import ServerController
from accord_client.helper import data_builder as DataBuilder, icon_builder as IconBuilder
from accord_client.model import AccordServer
from accord_client.ui import ui_main
from accord_client.controller import network_service as NetworkService

conn = ServerController()


class AccordMainWindow(QMainWindow, ui_main.Ui_AccordMainWindow):

    def __init__(self, app: QApplication):
        super(AccordMainWindow, self).__init__()
        self.setupUi(self)
        self.app = app

        self.setWindowTitle(AppName)
        self.setWindowIcon(IconBuilder.getImageQIcon(IconsMap.logo.value))

        isServersDataReady: bool = False
        while (not isServersDataReady):
            isServersDataReady = self.updateServers()
        self.connectSlot()

    def connectSlot(self):
        self.serversList.doubleClicked.connect(self.handelListEnterServer)
        self.buttonServerEnter.clicked.connect(self.handelButtonEnterServer)

    def updateServers(self) -> bool:
        dialog = QMessageBox(self)
        dialog.setWindowTitle("网络错误")
        dialog.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, on=True)
        code = 0

        try:
            model = AccordServer.ServerDataModel()
            serverList = NetworkService.getServerList()
            data = []
            for s in serverList:
                data.append(DataBuilder.server(s))

            model.setServerData(data)
            self.serversList.setModel(model)

        except Timeout:
            dialog.setText("获取服务器信息超时")
            code = dialog.exec()
        except Exception as e:
            dialog.setText("获取服务器信息错误\n" + e.__str__())
            code = dialog.exec()
        finally:
            if (code == 0):
                return True
            elif (code == QMessageBox.StandardButton.Cancel):
                self.destroy()
                self.deleteLater()
                return True
            else:
                return False

    def closeEvent(self, ev):
        ev.accept()

    def handelListEnterServer(self, curIndex: QModelIndex):
        if (curIndex.isValid()):
            serverData: AccordServer.ServerData = self.serversList.model().data(curIndex, Qt.ItemDataRole.UserRole)
            conn.enter(serverData)
        else:
            dialog = QMessageBox(self)
            dialog.setText("未选择正确的服务器")
            dialog.exec()

    def handelButtonEnterServer(self):
        indexes = self.serversList.selectedIndexes()
        if (len(indexes) > 0):
            serverData: AccordServer.ServerData = self.serversList.model().data(indexes[0], Qt.ItemDataRole.UserRole)
            conn.enter(serverData)
        else:
            dialog = QMessageBox(self)
            dialog.setText("未选择正确的服务器")
            dialog.exec()

    def handleAfterEnterServer(self, result):
        pass
