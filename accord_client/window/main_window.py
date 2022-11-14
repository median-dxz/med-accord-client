import os
import time
from datetime import datetime

from PyQt6 import QtWidgets
from PyQt6.QtCore import QFileInfo, QModelIndex, Qt, QTimerEvent
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
from accord_client.window.dialog_create_server import DialogCreateServer

client = ClientController()
member = MemberController()


class AccordMainWindow(QMainWindow, ui_main.Ui_AccordMainWindow):
    def __init__(self, app: QApplication):
        super(AccordMainWindow, self).__init__()
        self.promise = None
        self.setupUi(self)
        self.app = app

        self.setWindowTitle(Accord.__appname__)
        self.setWindowIcon(QIcon(PixmapBuilder.fromPath(Accord.Icons.LOGO)))

        isServersDataReady: bool = False
        while not isServersDataReady:
            isServersDataReady = self.updateServers()

        self.widgetMessage.setStyleSheet("background-color: #fff;")

        self.labelAvatar = AvatarLabel(self)
        self.layout_userInfo.insertWidget(0, self.labelAvatar)

        self.layout_message = QVBoxLayout(self.widgetMessage)
        self.layout_message.setDirection(QVBoxLayout.Direction.BottomToTop)
        self.layout_message.setContentsMargins(8, 8, 8, 8)
        self.layout_message.setSpacing(0)
        self.layout_message.addStretch()

        self.connectSlot()

        if member.hash == "":
            dialog = QMessageBox(
                QMessageBox.Icon.Warning,
                "无效的用户hash",
                "请通过下方按钮更新用户hash",
                parent=self,
            )
            dialog.open()
        else:
            self.labelHash.setText(f"#{member.hash}")

        self.textInputName.setText(member.name)
        self.labelAvatar.setAvatar(member.getAvatarPixmap())

        self.dialogCreateServer = DialogCreateServer(self)
        self.dialogWaitingAcceptEnter = QMessageBox(
            QMessageBox.Icon.Information,
            "加入服务器",
            "",
            parent=self,
        )
        button = QtWidgets.QPushButton("确认", self.dialogWaitingAcceptEnter)
        button.setDisabled(True)
        self.dialogWaitingAcceptEnter.addButton(
            button, QMessageBox.ButtonRole.AcceptRole
        )

    def connectSlot(self):
        self.listServers.doubleClicked.connect(self.onServerListDoubleClicked)
        self.buttonServerEnter.clicked.connect(self.onButtonServerEnterClicked)
        self.buttonServerLeave.clicked.connect(client.leave)
        self.buttonServerCreate.clicked.connect(self.onButtonServerCreateClicked)
        self.buttonSendMessage.clicked.connect(self.onButtonSendMessageClicked)
        self.buttonSendImage.clicked.connect(self.onButtonSendImageClicked)
        self.buttonRequireHash.clicked.connect(self.onButtonRequireHashClicked)
        self.buttonSettings.clicked.connect(self.onButtonSettingsClicked)
        self.labelAvatar.doubleClicked.connect(self.changeAvatar)
        self.textInputName.editingFinished.connect(self.changeMemberName)

        self.editMessageContent.textChanged.connect(
            lambda: self.browserMessageContent.setMarkdown(
                f"**预览模式:** <br/>" + self.editMessageContent.toPlainText()
            )
        )
        self.buttonEditMessage.clicked.connect(
            lambda: self.stackedMessageEdit.setCurrentIndex(0)
        )
        self.buttonPreviewMessage.clicked.connect(
            lambda: self.stackedMessageEdit.setCurrentIndex(1)
        )
        client.emitReceiveCtrlMsg.connect(self.setStatusLabel)
        client.emitUpdateMembersList.connect(self.updateMembersList)
        client.emitReceiveMessages.connect(self.handleReceiveMessages)
        client.emitAcceptEnter.connect(self.handleAfterEnterServer)
        client.emitDisconnected.connect(self.handleAfterLeaveServer)
        member.emitUpdateHash.connect(self.labelHash.setText)
        member.emitUpdateInfo.connect(self.handleUpdateMemberInfo)

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

    def closeEvent(self, ev):
        if client.online:
            self.promise = SignalWaiter(client.emitAcceptEnter, lambda: client.leave())
            self.promise.then(ev.accept)
        else:
            ev.accept()

    def timerEvent(self, e: QTimerEvent) -> None:
        if e.timerId() == self.timerAcceptEnter:
            self.dialogWaitingAcceptEnter.accept()
            self.killTimer(self.timerAcceptEnter)
        return super().timerEvent(e)

    def updateMembersList(self, membersList):
        model = AccordModel.MembersListModel()
        model.setMembersList(membersList)
        self.listMembers.setModel(model)

    def setStatusLabel(self, msg, action):
        now = datetime.now()
        time_str = now.strftime("%m-%d %H:%M:%S")
        self.labelStatus.setText(f"[{time_str}] {action}: {msg}")

    def changeAvatar(self):
        try:
            file_name, pix, file_size = PixmapBuilder.selectImageFile(self)

            if file_size > 64 * 1024:  # 64KB
                QMessageBox(
                    QMessageBox.Icon.Warning, "无法上传", "头像文件大小超过限制(>64KB)", parent=self
                ).open()
                raise Exception("size too large")
            member.avatar = PixmapBuilder.toBase64fromPath(file_name)
            self.labelAvatar.setAvatar(pix)
        except Exception:
            pass

    def changeMemberName(self):
        new_name = self.textInputName.text()
        if member.name == new_name:
            return
        result = QMessageBox(
            QMessageBox.Icon.Question,
            "更改用户名",
            f"确定要将名称改为{new_name}吗?",
            QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Yes,
            self,
        ).exec()
        if result == QMessageBox.StandardButton.Yes:
            member.name = new_name
        elif result == QMessageBox.StandardButton.Discard:
            self.textInputName.setText(member.name)

    def onServerListDoubleClicked(self, curIndex: QModelIndex):
        if curIndex.isValid():
            self.handleEnterServer(curIndex)

    def onButtonServerEnterClicked(self):
        indexes = self.listServers.selectedIndexes()
        if len(indexes) == 1:
            self.handleEnterServer(indexes[0])

    def onButtonSendMessageClicked(self):
        text = self.editMessageContent.toPlainText()
        if (text != "") & (client.online):
            self.handleSendMessage(text)
            self.editMessageContent.setText("")

    def onButtonSendImageClicked(self):
        if not (client.online):
            return
        try:
            file_name, _, _ = PixmapBuilder.selectImageFile(self)
            byteData = PixmapBuilder.toBase64fromPath(file_name)
            client.sendImage(byteData)
        except Exception as e:
            print(e)

    def onButtonRequireHashClicked(self):
        if client.online:
            dialog = QMessageBox(
                QMessageBox.Icon.Warning, "Accord", "更换用户hash前,请先退出当前服务器", parent=self
            )
            dialog.open()
        else:
            member.updateMemberHash()

    def onButtonServerCreateClicked(self):
        self.dialogCreateServer.show()

    def onButtonSettingsClicked(self):
        path = os.path.join(Accord.baseDir, "config/global.ini")
        if not QFileInfo(path).exists():
            QMessageBox.warning(self, "Accord", "配置文件丢失")
        os.startfile(path)

    def handleEnterServer(self, curIndex: QModelIndex):
        serverData: AccordData.ServerData = self.listServers.model().data(
            curIndex, Qt.ItemDataRole.UserRole
        )

        def enter():
            client.enter(serverData)
            self.dialogWaitingAcceptEnter.setText(format(serverData) + "\n正在加入中...")
            self.dialogWaitingAcceptEnter.open()

        if (serverData.hash != client.serverData.hash) & (client.serverData.hash != ""):
            self.promise = SignalWaiter(client.emitDisconnected, client.leave)
            self.promise.then(enter)
        elif client.serverData.hash == "":
            enter()

    def handleAfterEnterServer(self):
        self.dialogWaitingAcceptEnter.setText(format(client.serverData) + "\n已加入")
        self.labelServerName.setText(format(client.serverData))
        client.updateMemberList()
        client.getHistoryMessage()
        self.timerAcceptEnter = self.startTimer(800)

    def handleAfterLeaveServer(self):
        while not self.layout_message.itemAt(1) is None:
            item = self.layout_message.itemAt(1)
            self.layout_message.removeItem(item)
            item.widget().deleteLater()
        self.widgetMessage.update()
        self.labelServerName.setText("未加入服务器")
        self.updateMembersList([])

    def handleSendMessage(self, text: str):
        client.send(text)

    def handleReceiveMessages(self, messages: list[AccordData.MessageData]):
        for message in messages:
            message_widget = Message(self)
            message_widget.hide()  # 降低动态插入控件在自动调整大小时的刷新闪烁
            self.layout_message.insertWidget(1, message_widget)
            message_widget.show()
            message_widget.setMessage(message)

    def handleUpdateMemberInfo(self):
        if client.online:
            client.setMemberInfo()
