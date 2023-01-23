import os
import signal
import threading


class MyTimer():
    def __init__(self, timeout=10):
        self.timeout = timeout
        self._t = None

    def _expire(self):
        print("\nWatchdog: time expired: ")
        os.kill(os.getpid(), signal.SIGTERM)

    def start(self):
        if self._t is None:
            self._t = threading.Timer(self.timeout, self._expire)
            self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None
