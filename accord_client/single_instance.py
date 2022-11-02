from PyQt6.QtNetwork import QLocalServer, QLocalSocket


class SingleInstance:
    def __init__(self, appid, allow=False):
        self._appid = appid
        self._is_running = False
        self._server = None

        if allow == True:
            return

        local_socket = QLocalSocket()
        local_socket.connectToServer(appid)

        self._is_running = local_socket.waitForConnected()
        if self._is_running:
            local_socket.disconnectFromServer()
        else:
            error = local_socket.error()
            if error == QLocalSocket.LocalSocketError.ConnectionRefusedError:
                QLocalServer.removeServer(self._appid)
            self._server = QLocalServer()
            self._server.listen(self._appid)
            self._server.newConnection.connect(self._on_new_connection)
        local_socket.close()

    def close(self):
        if self._server:
            self._server.close()

    def is_running(self):
        return self._is_running

    def _on_new_connection(self):
        if not self._server:
            return
        in_socket = self._server.nextPendingConnection()
        if not in_socket:
            return
        in_socket.disconnectFromServer()
        in_socket.close()
