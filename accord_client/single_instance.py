from PyQt6.QtNetwork import QLocalServer, QLocalSocket


class SingleInstance:
    def __init__(self, appid):
        self._appid = appid
        self._isRunning = False
        self._server = None
        localSocket = QLocalSocket()
        localSocket.connectToServer(appid)

        self._isRunning = localSocket.waitForConnected()
        if self._isRunning:
            localSocket.disconnectFromServer()
        else:
            error = localSocket.error()
            if error == QLocalSocket.LocalSocketError.ConnectionRefusedError:
                QLocalServer.removeServer(self._appid)
            self._server = QLocalServer()
            self._server.listen(self._appid)
            self._server.newConnection.connect(self._onNewConnection)
        localSocket.close()

    def close(self):
        if self._server:
            self._server.close()

    def isRunning(self):
        return self._isRunning

    def _onNewConnection(self):
        if not self._server:
            return
        inSocket = self._server.nextPendingConnection()
        if not inSocket:
            return
        inSocket.disconnectFromServer()
        inSocket.close()
