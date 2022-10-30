from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QColor, QPalette, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from requests.exceptions import Timeout

import accord_client as Accord

import accord_client.helper.icon_builder as IconBuilder

from accord_client.helper import data_builder as DataBuilder
from accord_client.helper.signal_waiter import SignalWaiter
from accord_client.model import AccordServer
from accord_client.provider import client_controller as ClientController
from accord_client.provider import member_controller as MemberController
from accord_client.provider import network_service as NetworkService
from accord_client.ui import ui_main
from accord_client.widget.AvatarLabel import AvatarLabel

conn = ClientController.ClientController()
user = MemberController.MemberController()


class AccordMainWindow(QMainWindow, ui_main.Ui_AccordMainWindow):

    def __init__(self, app: QApplication):
        super(AccordMainWindow, self).__init__()
        self.setupUi(self)
        self.app = app

        self.setWindowTitle(Accord.__appname__)
        self.setWindowIcon(QIcon(IconBuilder.getQPixmapFromPath(Accord.IconsMap.logo.value)))

        # palette = self.palette()
        # palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Window, QColor(255, 255, 255))
        # self.setPalette(palette)

        isServersDataReady: bool = False
        while (not isServersDataReady):
            isServersDataReady = self.updateServers()

        self.labelAvatar = AvatarLabel(self)
        self.horizontalLayout_userInfo.insertWidget(0, self.labelAvatar)

        self.connectSlot()

        if user.getMemberHash() == "":
            dialog = QMessageBox(title="无效的用户hash", text="请通过下方按钮更新用户hash", icon=QMessageBox.Icon.Warning, parent=self)
            dialog.exec()
        else:
            self.labelHash.setText(f"#{user.getMemberHash()}")

        self.textInputName.setText(user.getName())
        self.labelAvatar.setAvatar(user.getAvatarPixmap())

    def connectSlot(self):
        self.serversList.doubleClicked.connect(self.onServerListDoubleClicked)
        self.buttonServerEnter.clicked.connect(self.onButtonServerEnterClicked)
        self.buttonRequireHash.clicked.connect(user.updateMemberHash)
        self.buttonServerLeave.clicked.connect(conn.leave)

        user.emitUpdateHash.connect(self.labelHash.setText)

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

    def onServerListDoubleClicked(self, curIndex: QModelIndex):
        self.handleEnterServer(curIndex.isValid(), curIndex)

    def onButtonServerEnterClicked(self):
        indexes = self.serversList.selectedIndexes()
        self.handleEnterServer(len(indexes) > 0, indexes[0])

    def handleEnterServer(self, valid: bool, curIndex: QModelIndex):
        if (not valid):
            dialog = QMessageBox(text="未选择正确的服务器", title="服务器进入失败", icon=QMessageBox.Icon.Warning, parent=self)
            dialog.exec()
        else:
            serverData: AccordServer.ServerData = self.serversList.model().data(curIndex, Qt.ItemDataRole.UserRole)
            if (serverData.hash != conn.serverData.hash) & (conn.serverData.hash != ""):
                self.promise = SignalWaiter(conn.emitDisconnected, conn.leave)
                self.promise.then(lambda: conn.enter(serverData))
            elif conn.serverData.hash == "":
                conn.enter(serverData)

    def handleAfterEnterServer(self, result):
        pass

    def handleAfterLeaveServer(self, result):
        pass
