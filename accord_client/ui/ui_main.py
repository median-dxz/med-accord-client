# Form implementation generated from reading ui file './accord_client/ui/main.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AccordMainWindow(object):
    def setupUi(self, AccordMainWindow):
        AccordMainWindow.setObjectName("AccordMainWindow")
        AccordMainWindow.resize(1246, 811)
        self.centralwidget = QtWidgets.QWidget(AccordMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainGridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.mainGridLayout.setContentsMargins(0, 0, 0, 0)
        self.mainGridLayout.setSpacing(0)
        self.mainGridLayout.setObjectName("mainGridLayout")
        self.mainArea = QtWidgets.QHBoxLayout()
        self.mainArea.setObjectName("mainArea")
        self.serverView = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverView.sizePolicy().hasHeightForWidth())
        self.serverView.setSizePolicy(sizePolicy)
        self.serverView.setMinimumSize(QtCore.QSize(192, 0))
        self.serverView.setObjectName("serverView")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.serverView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listServers = QtWidgets.QListView(self.serverView)
        self.listServers.setObjectName("listServers")
        self.verticalLayout.addWidget(self.listServers)
        self.line = QtWidgets.QFrame(self.serverView)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.buttonServerEnter = QtWidgets.QPushButton(self.serverView)
        self.buttonServerEnter.setObjectName("buttonServerEnter")
        self.verticalLayout.addWidget(self.buttonServerEnter)
        self.buttonServerLeave = QtWidgets.QPushButton(self.serverView)
        self.buttonServerLeave.setObjectName("buttonServerLeave")
        self.verticalLayout.addWidget(self.buttonServerLeave)
        self.buttonServerCreate = QtWidgets.QPushButton(self.serverView)
        self.buttonServerCreate.setObjectName("buttonServerCreate")
        self.verticalLayout.addWidget(self.buttonServerCreate)
        self.mainArea.addWidget(self.serverView)
        self.messageView = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageView.sizePolicy().hasHeightForWidth())
        self.messageView.setSizePolicy(sizePolicy)
        self.messageView.setObjectName("messageView")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.messageView)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.areaMessage = QtWidgets.QScrollArea(self.messageView)
        self.areaMessage.setWidgetResizable(True)
        self.areaMessage.setObjectName("areaMessage")
        self.widgetMessage = QtWidgets.QWidget()
        self.widgetMessage.setGeometry(QtCore.QRect(0, 0, 664, 583))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetMessage.sizePolicy().hasHeightForWidth())
        self.widgetMessage.setSizePolicy(sizePolicy)
        self.widgetMessage.setObjectName("widgetMessage")
        self.areaMessage.setWidget(self.widgetMessage)
        self.verticalLayout_2.addWidget(self.areaMessage)
        self.areaMessageEdit = QtWidgets.QWidget(self.messageView)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.areaMessageEdit.sizePolicy().hasHeightForWidth())
        self.areaMessageEdit.setSizePolicy(sizePolicy)
        self.areaMessageEdit.setMaximumSize(QtCore.QSize(16777215, 128))
        self.areaMessageEdit.setObjectName("areaMessageEdit")
        self.layout_areaMessageEdit = QtWidgets.QGridLayout(self.areaMessageEdit)
        self.layout_areaMessageEdit.setContentsMargins(0, 0, 0, 0)
        self.layout_areaMessageEdit.setObjectName("layout_areaMessageEdit")
        self.buttonEditMessage = QtWidgets.QPushButton(self.areaMessageEdit)
        self.buttonEditMessage.setObjectName("buttonEditMessage")
        self.layout_areaMessageEdit.addWidget(self.buttonEditMessage, 0, 0, 1, 1)
        self.buttonPreviewMessage = QtWidgets.QPushButton(self.areaMessageEdit)
        self.buttonPreviewMessage.setObjectName("buttonPreviewMessage")
        self.layout_areaMessageEdit.addWidget(self.buttonPreviewMessage, 0, 1, 1, 1)
        self.buttonSendMessage = QtWidgets.QPushButton(self.areaMessageEdit)
        self.buttonSendMessage.setObjectName("buttonSendMessage")
        self.layout_areaMessageEdit.addWidget(self.buttonSendMessage, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.layout_areaMessageEdit.addItem(spacerItem, 0, 2, 1, 1)
        self.stackedMessageEdit = QtWidgets.QStackedWidget(self.areaMessageEdit)
        self.stackedMessageEdit.setObjectName("stackedMessageEdit")
        self.editMessageContent = QtWidgets.QTextEdit()
        self.editMessageContent.setObjectName("editMessageContent")
        self.stackedMessageEdit.addWidget(self.editMessageContent)
        self.browserMessageContent = QtWidgets.QTextBrowser()
        self.browserMessageContent.setObjectName("browserMessageContent")
        self.stackedMessageEdit.addWidget(self.browserMessageContent)
        self.layout_areaMessageEdit.addWidget(self.stackedMessageEdit, 1, 0, 1, 4)
        self.verticalLayout_2.addWidget(self.areaMessageEdit)
        self.mainArea.addWidget(self.messageView)
        self.userView = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userView.sizePolicy().hasHeightForWidth())
        self.userView.setSizePolicy(sizePolicy)
        self.userView.setMinimumSize(QtCore.QSize(192, 0))
        self.userView.setObjectName("userView")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.userView)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelServerName = QtWidgets.QLabel(self.userView)
        self.labelServerName.setObjectName("labelServerName")
        self.verticalLayout_3.addWidget(self.labelServerName)
        self.listMembers = QtWidgets.QListView(self.userView)
        self.listMembers.setObjectName("listMembers")
        self.verticalLayout_3.addWidget(self.listMembers)
        self.mainArea.addWidget(self.userView)
        self.mainGridLayout.addLayout(self.mainArea, 0, 0, 1, 1)
        self.footerLayout = QtWidgets.QHBoxLayout()
        self.footerLayout.setContentsMargins(4, 4, 4, 4)
        self.footerLayout.setSpacing(12)
        self.footerLayout.setObjectName("footerLayout")
        self.userInfo = QtWidgets.QFrame(self.centralwidget)
        self.userInfo.setObjectName("userInfo")
        self.layout_userInfo = QtWidgets.QHBoxLayout(self.userInfo)
        self.layout_userInfo.setObjectName("layout_userInfo")
        self.textInputName = QtWidgets.QLineEdit(self.userInfo)
        self.textInputName.setObjectName("textInputName")
        self.layout_userInfo.addWidget(self.textInputName)
        self.buttonRequireHash = QtWidgets.QPushButton(self.userInfo)
        self.buttonRequireHash.setObjectName("buttonRequireHash")
        self.layout_userInfo.addWidget(self.buttonRequireHash)
        self.labelHash = QtWidgets.QLabel(self.userInfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHash.sizePolicy().hasHeightForWidth())
        self.labelHash.setSizePolicy(sizePolicy)
        self.labelHash.setMinimumSize(QtCore.QSize(72, 0))
        self.labelHash.setObjectName("labelHash")
        self.layout_userInfo.addWidget(self.labelHash)
        self.footerLayout.addWidget(self.userInfo)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.footerLayout.addItem(spacerItem1)
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.footerLayout.addWidget(self.labelStatus)
        self.buttonSettings = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSettings.sizePolicy().hasHeightForWidth())
        self.buttonSettings.setSizePolicy(sizePolicy)
        self.buttonSettings.setObjectName("buttonSettings")
        self.footerLayout.addWidget(self.buttonSettings)
        self.mainGridLayout.addLayout(self.footerLayout, 1, 0, 1, 1)
        AccordMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AccordMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 22))
        self.menubar.setObjectName("menubar")
        AccordMainWindow.setMenuBar(self.menubar)

        self.retranslateUi(AccordMainWindow)
        self.stackedMessageEdit.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AccordMainWindow)

    def retranslateUi(self, AccordMainWindow):
        _translate = QtCore.QCoreApplication.translate
        AccordMainWindow.setWindowTitle(_translate("AccordMainWindow", "AccordMainWindow"))
        self.buttonServerEnter.setText(_translate("AccordMainWindow", "加入服务器"))
        self.buttonServerLeave.setText(_translate("AccordMainWindow", "离开服务器"))
        self.buttonServerCreate.setText(_translate("AccordMainWindow", "创建服务器"))
        self.buttonEditMessage.setText(_translate("AccordMainWindow", "编辑"))
        self.buttonPreviewMessage.setText(_translate("AccordMainWindow", "预览"))
        self.buttonSendMessage.setText(_translate("AccordMainWindow", "发送"))
        self.labelServerName.setText(_translate("AccordMainWindow", "未加入服务器"))
        self.buttonRequireHash.setText(_translate("AccordMainWindow", "更新hash"))
        self.labelHash.setText(_translate("AccordMainWindow", "# "))
        self.buttonSettings.setText(_translate("AccordMainWindow", "设置"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AccordMainWindow = QtWidgets.QMainWindow()
    ui = Ui_AccordMainWindow()
    ui.setupUi(AccordMainWindow)
    AccordMainWindow.show()
    sys.exit(app.exec())
