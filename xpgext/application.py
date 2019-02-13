import pygame
from pygame.locals import *


class XPGEApplication:
    """
    Base class for the application using XPG Extensions.

    :param scene_manager: scene manager implementation used in the application
    :param resolution: the target resolution of the pygame window
    :param args: arguments passed to pygame.display.set_mode
    :param kwargs: keyword arguments passed to pygame.display.set_mode
    """

    def __init__(self, scene_manager, resolution, *args, **kwargs):
        self._surface = pygame.display.set_mode(resolution, *args, **kwargs)
        self._clock = pygame.time.Clock()

        self._scene_manager = scene_manager
        self._frame_rate = 30
        self._is_running = False

    @property
    def scene_manager(self):
        """
        The scene manager used by the application.
        """

        return self._scene_manager

    @property
    def frame_rate(self):
        """
        The desired frame rate.

        This property does not return the computed, real frame rate on which the application currently runs,
        but the desired value.
        """

        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, value):
        self._frame_rate = value

    @property
    def is_running(self):
        """
        The state of the application.

        This property returns True if the mainloop of the application is running, and False otherwise.
        """

        return self._is_running

    def on_quit(self):
        """Method called on pygame.QUIT event."""

        self._is_running = False

    def run_main_loop(self):
        """Run the main loop of the application."""

        self._is_running = True
        while self._is_running:
            self._clock.tick(self._frame_rate)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.on_quit()
                else:
                    self._scene_manager.handle_event(event)
            self._scene_manager.update()
            self._scene_manager.draw(self._surface)
            pygame.display.flip()
