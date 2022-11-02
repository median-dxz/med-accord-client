from enum import Enum

from PyQt6.QtCore import QObject, pyqtBoundSignal, pyqtSignal


class SignalWaiter(QObject):

    class State(Enum):
        PENDING = ...
        FULFILLED = ...

    def __init__(self, signal: pyqtBoundSignal, executor) -> None:
        super().__init__()
        self.state = self.State.PENDING
        self.signal = signal

        self.signal.connect(self.resolver)
        self.callback = None
        executor()

    def then(self, callback):
        if self.state == self.State.PENDING:
            self.callback = callback
        elif self.state == self.State.FULFILLED:
            callback()

    def resolver(self):
        self.state = self.State.FULFILLED
        if not self.callback is None:
            self.callback()
        self.signal.disconnect(self.resolver)
        self.deleteLater()
