import threading

class wasig():
    def __init__(self):
        self._event = threading.Event()

    def wait_signal(self):
        self._event.wait()
        self._event.clear()

    def signal(self):
        self._event.set()