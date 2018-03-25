import pygame
from pygame.locals import *


class Sprite(pygame.sprite.Sprite):

    def __init__(self, scene_manager, *groups):
        super().__init__(groups)
        self.scene_manager = scene_manager
        self.image = None
        self.rect = None
        self.active = True
        self.take_focus = True
        self.interacts_with_mouse = True
        self.behaviour = None

        self._previous_focus = False
        self.focus = False

    def load_image(self, path):
        """
        Load image from the given path.

        :param path: path to an image file
        :type path: str
        """

        self.image = pygame.image.load(path).convert()
        self.rect = self.image.get_rect()

    def update(self):
        if self.behaviour is not None and self.active:
            self.behaviour.on_update()

    def handle_event(self, event):
        handled = False
        if not self.active:
            return None

        if self.take_focus:
            mouse_pos = pygame.mouse.get_pos()
            self._previous_focus = self.focus
            if self.rect.collidepoint(mouse_pos):
                self.focus = True
            else:
                self.focus = False
            if self.behaviour is not None and self.focus is not self._previous_focus:
                if self.focus:
                    self.behaviour.on_hover()
                elif not self.focus:
                    self.behaviour.on_hover_exit()

        if event.type == MOUSEBUTTONUP and self.focus:
            if self.behaviour is not None:
                self.behaviour.on_click(event.button)
                handled = True

        if self.behaviour is not None:
            handled = self.behaviour.on_handle_event(event)

        return handled

    def draw(self, surface):
        """
        Draw the sprite onto the given surface.

        :param surface: the destination surface
        :type surface: pygame.Surface
        """

        if self.active:
            surface.blit(self.image, self.rect.topleft)

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)


class SpriteBehaviour:
    """
    Base class for scripts controlling sprite behaviour.

    Override the appropriate method and instantiate the descendant of this class
    to Sprite.behaviour.
    """

    def __init__(self, sprite):
        self.sprite = sprite

    def on_update(self):
        """Method called on Sprite.update."""

    def on_handle_event(self, event):
        """
        Method called on Sprite.handle_event.

        It is advised not to use this method to handle on_click, on_hover and on_hover_exit.
        Override the corresponding methods instead. This method may return True if you wish
        the game manager to stop checking if any sprite handled the given event after this call.
        """

    def on_click(self, button):
        """
        Method called on Sprite.handle_event, when the sprite has been clicked.

        :param button: mouse button that fired this event
        :type button: int
        """

    def on_hover(self):
        """
        Method called on Sprite.handle_event, when mouse pointer starts colliding with the sprite.
        """

    def on_hover_exit(self):
        """
        Method called on Sprite.handle_event, when mouse pointer stops colliding with the sprite.
        """


class Group(pygame.sprite.Group):
    """Group implementation adjusted to work with XPGE Sprite."""

    def __init__(self, *sprites):
        super().__init__(sprites)

    def handle_event(self, event):
        """
        Pass the event to each of the scene elements until one of them handles the event.

        :param event: event to handle
        :type event: pygame.event.Event
        """

        handled = False
        for sprite in reversed(self.sprites()):
            if sprite.handle_event(event):
                handled = True
                break
        return handled

    def update(self, *args):
        """
        Update all the scene elements. Called every frame.
        """

        for sprite in reversed(self.sprites()):
            sprite.update(args)

    def draw(self, surface):
        """
        Draw all the scene elements on the given surface.

        :param surface: the pygame main surface
        :type surface: pygame.Surface
        """

        for sprite in reversed(self.sprites()):
            sprite.draw(surface)
