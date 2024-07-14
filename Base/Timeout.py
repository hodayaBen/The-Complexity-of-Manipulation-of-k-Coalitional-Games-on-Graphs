import multiprocessing
from multiprocessing import TimeoutError
import signal

class Timeout():
    """
    Allows polling a function till success or timeout::

        import time
        from magneto.utils import Timeout

        result = False

        with Timeout(seconds=5):
            while not result:
                result = some_function()
                time.time()sleep(0.5)


    :param integer seconds: Timeout value in seconds. Defaults to 1.
    :param str error_message: Error message to display when timeout occurs. Defaults to 'Timeout'.
    """

    def __init__(self, seconds=1, error_message='Timeout occured B'):
        self.seconds = seconds or 1
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        print('handling timeout A')
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)
