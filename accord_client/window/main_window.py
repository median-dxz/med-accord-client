from datetime import datetime

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout
from requests.exceptions import Timeout

import accord_client as Accord
import accord_client.model.data as AccordData
import accord_client.model.model as AccordModel
from accord_client import DataBuilder, PixmapBuilder, SignalWaiter
from accord_client import http_service as HttpService
from accord_client.client import ClientController
from accord_client.member import MemberController
from accord_client.ui import ui_main
from accord_client.widget.AvatarLabel import AvatarLabel
from accord_client.widget.Message import Message

client = ClientController()
member = MemberController()


class AccordMainWindow(QMainWindow, ui_main.Ui_AccordMainWindow):
    def __init__(self, app: QApplication):
        super(AccordMainWindow, self).__init__()
        self.promise = None
        self.setupUi(self)
        self.app = app

        self.setWindowTitle(Accord.__appname__)
        self.setWindowIcon(QIcon(PixmapBuilder.getQPixmapFromPath(Accord.Icons.LOGO)))

        # palette = self.palette()
        # palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Window, QColor(255, 255, 255))
        # self.setPalette(palette)

        isServersDataReady: bool = False
        while not isServersDataReady:
            isServersDataReady = self.updateServers()

        self.labelAvatar = AvatarLabel(self)
        self.layout_userInfo.insertWidget(0, self.labelAvatar)

        self.layout_message = QVBoxLayout(self.widgetMessage)
        self.layout_message.setDirection(QVBoxLayout.Direction.BottomToTop)
        self.layout_message.addStretch()

        self.connectSlot()

        if member.hash == "":
            dialog = QMessageBox(
                title="无效的用户hash",
                text="请通过下方按钮更新用户hash",
                icon=QMessageBox.Icon.Warning,
                parent=self,
            )
            dialog.exec()
        else:
            self.labelHash.setText(f"#{member.hash}")

        self.textInputName.setText(member.name)
        self.labelAvatar.setAvatar(member.getAvatarPixmap())

    def connectSlot(self):
        self.listServers.doubleClicked.connect(self.onServerListDoubleClicked)
        self.buttonServerEnter.clicked.connect(self.onButtonServerEnterClicked)
        self.buttonServerLeave.clicked.connect(client.leave)
        self.buttonRequireHash.clicked.connect(member.updateMemberHash)
        client.emitReceiveCtrlMsg.connect(self.setStatusLabel)
        client.emitUpdateMembersList.connect(self.updateMembersList)
        client.emitAcceptEnter.connect(self.handleAfterEnterServer)
        client.emitDisconnected.connect(self.handleAfterLeaveServer)

        member.emitUpdateHash.connect(self.labelHash.setText)

    def updateServers(self) -> bool:
        dialog = QMessageBox(
            QMessageBox.Icon.Warning,
            "网络错误",
            "error",
            QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel,
            self,
        )

        dialog.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, on=True)
        code = 0

        try:
            model = AccordModel.ServerDataModel()
            serverList = HttpService.get_server_list()
            data = []
            for s in serverList:
                data.append(DataBuilder.server(s))

            model.setServerData(data)
            self.listServers.setModel(model)

        except Timeout:
            dialog.setText("获取服务器信息超时")
            code = dialog.exec()
        except Exception as e:
            dialog.setText("获取服务器信息错误\n" + str(e))
            code = dialog.exec()
        finally:
            if code == 0:
                return True

            if code == QMessageBox.StandardButton.Cancel:
                self.destroy()
                self.deleteLater()
                return True
            else:
                return False

    def updateMembersList(self, membersList):
        model = AccordModel.MembersListModel()
        model.setMembersList(membersList)
        self.listMembers.setModel(model)
        value = client.serverData
        self.labelServerName.setText(
            f"{value.showName} - {value.actualName}#{value.hash}"
        )

    def closeEvent(self, ev):
        ev.accept()

    def setStatusLabel(self, msg, action):
        now = datetime.now()
        time_str = now.strftime("%m-%d %H:%M:%S")
        self.labelStatus.setText(f"[{time_str}] {action}: {msg}")

    def onServerListDoubleClicked(self, curIndex: QModelIndex):
        self.handleEnterServer(curIndex.isValid(), curIndex)

    def onButtonServerEnterClicked(self):
        indexes = self.listServers.selectedIndexes()
        self.handleEnterServer(len(indexes) > 0, indexes[0])

    def onButtonSendMessageClicked(self):
        self.handleSendMessage()

    def handleEnterServer(self, valid: bool, curIndex: QModelIndex):
        if not valid:
            dialog = QMessageBox(
                text="未选择正确的服务器",
                title="服务器进入失败",
                icon=QMessageBox.Icon.Warning,
                parent=self,
            )
            dialog.exec()
        else:
            serverData: AccordData.ServerData = self.listServers.model().data(
                curIndex, Qt.ItemDataRole.UserRole
            )
            if (serverData.hash != client.serverData.hash) & (
                client.serverData.hash != ""
            ):
                self.promise = SignalWaiter(client.emitDisconnected, client.leave)
                self.promise.then(lambda: client.enter(serverData))
            elif client.serverData.hash == "":
                client.enter(serverData)

    def handleAfterEnterServer(self):
        self.buttonSendMessage.clicked.connect(self.onButtonSendMessageClicked)

    def handleAfterLeaveServer(self):
        self.buttonSendMessage.clicked.disconnect(self.onButtonSendMessageClicked)

    def handleSendMessage(self):
        m = Message(self)
        m.hide()
        self.layout_message.addWidget(m)
        m.show()
