"""
Utilities for testing.
"""

from threading import Thread
from time import sleep

from pygame import quit as pygame_quit
from pygame import error as PygameError


def run_with_timeout(timeout, test_func, *args, **kwargs):
    """
    Run the given test_func and quit pygame after the given timeout.

    This util method helps to test various functionalities that happen in the main loop of the pygame application.

    :param timeout: the amount of time after which the pygame should be stopped
    :param test_func: the function with the loop
    :param args: args passed to the test_func
    :param kwargs: kwargs passed to the test_func
    """

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
        test_func(*args, **kwargs)
    except PygameError:
        pass
