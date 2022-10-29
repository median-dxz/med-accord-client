from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from requests.exceptions import Timeout

from accord_client import IconsMap
from accord_client import __appname__ as AppName
from accord_client.helper import data_builder as DataBuilder
from accord_client.helper import icon_builder as IconBuilder
from accord_client.helper.signal_waiter import SignalWaiter
from accord_client.model import AccordServer
from accord_client.provider import client_controller as ClientController
from accord_client.provider import network_service as NetworkService
from accord_client.ui import ui_main

conn = ClientController.ClientController()


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
        self.serversList.doubleClicked.connect(self.serverListDoubleClicked)
        self.buttonServerEnter.clicked.connect(self.buttonServerEnterClicked)

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

    def serverListDoubleClicked(self, curIndex: QModelIndex):
        self.handleEnterServer(curIndex.isValid(), curIndex)

    def buttonServerEnterClicked(self):
        indexes = self.serversList.selectedIndexes()
        self.handleEnterServer(len(indexes) > 0, indexes[0])

    def handleEnterServer(self, valid: bool, curIndex: QModelIndex):
        if (valid):
            serverData: AccordServer.ServerData = self.serversList.model().data(curIndex, Qt.ItemDataRole.UserRole)
            self.promise = SignalWaiter(self)
            promise = self.promise
            promise.setCallback(lambda: conn.enter(serverData))
            if (serverData.hash != conn.serverData.hash) & (conn.serverData.hash != ""):
                promise.setSignal(conn.acceptLeave)
                promise.run(lambda: conn.leave())
            elif conn.serverData.hash == "":
                promise.run(lambda: {})
        else:
            dialog = QMessageBox(self)
            dialog.setText("未选择正确的服务器")
            dialog.exec()

    def handleAfterEnterServer(self, result):
        pass
