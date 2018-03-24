import pygame
from pygame.locals import *


class XPGApplication:
    """
    Base class for the application using XPG Extensions.

    :param scene_manager: scene manager implementation used in the application
    :type scene_manager: SceneManagerBase
    :param resolution: the target resolution of the pygame window
    :type resolution: tuple
    :param args: arguments passed to pygame.display.set_mode
    :param kwargs: keyword arguments passed to pygame.display.set_mode
    """

    def __init__(self, scene_manager, resolution, *args, **kwargs):
        self.scene_manager = scene_manager
        self.surface = pygame.display.set_mode(resolution, *args, **kwargs)

        self.running = False

    def on_quit(self):
        """Method called on pygame.QUIT event."""

        self.running = False

    def run_main_loop(self):
        """Run the main loop of the application."""
        
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.on_quit()
                else:
                    self.scene_manager.handle_event(event)
            self.scene_manager.update()
            self.scene_manager.draw(self.surface)
            pygame.display.flip()
