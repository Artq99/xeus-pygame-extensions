from unittest import TestCase

from threading import Thread
from time import sleep

from pygame import quit as pygame_quit
from pygame import error as PygameError


def run_with_timeout(timeout, test_func, *args, **qwargs):

    class _PyGameStopperThread(Thread):

        def __init__(self, stop_delay):
            super().__init__()
            self.stop_delay = stop_delay

        def run(self):
            sleep(self.stop_delay)
            pygame_quit()

    stopper_thread = _PyGameStopperThread(timeout)
    stopper_thread.start()

    try:
        test_func(*args, **qwargs)
    except PygameError:
        pass
