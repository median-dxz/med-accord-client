from PyQt6.QtCore import QObject, pyqtSignal, pyqtBoundSignal


class SignalWaiter(QObject):

    def __init__(self, parent) -> None:
        super().__init__()

    def setCallback(self, cb):
        self._callback = cb

    def run(self, fun):
        if (hasattr(self, "signal")):
            fun()
        else:
            self._callback()
            self.deleteLater()

    def resolver(self):
        self._callback()
        self.signal.disconnect(self.resolver)
        self.deleteLater()

    def setSignal(self, signal: pyqtBoundSignal):
        self.signal = signal
        signal.connect(self.resolver)