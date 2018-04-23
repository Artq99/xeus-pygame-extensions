import pygame
from pygame.locals import *


class Sprite(pygame.sprite.Sprite):
    """
    Base class for all the visible game elements.
    """

    def __init__(self, scene_manager, *groups):
        super().__init__(groups)
        self.scene_manager = scene_manager
        self.image = None
        self.rect = None
        self.active = True
        self.take_focus = True
        self.interacts_with_mouse = True
        self.components = list()

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
        """
        Update sprite and call on_update methods from each of its components.
        """

        if self.active:
            for component in self.components:
                component.on_update()

    def handle_event(self, event):
        """
        Handle the given event. It is passed to each of its components

        :param event: event
        :type event: pygame.event.Event
        """

        if not self.active:
            return False
        self._handle_mouse_motion(event)
        handled = self._handle_mouse_button_up(event)
        if not handled:
            for component in self.components:
                if component.on_handle_event(event):
                    handled = True

        return handled

    def _handle_mouse_motion(self, event):
        if event.type == MOUSEMOTION and self.take_focus:
            self._previous_focus = self.focus
            if self.rect.collidepoint(event.pos):
                self.focus = True
            else:
                self.focus = False
            if self.focus is not self._previous_focus:
                for component in self.components:
                    if self.focus:
                        component.on_hover()
                    else:
                        component.on_hover_exit()

    def _handle_mouse_button_up(self, event):
        if event.type == MOUSEBUTTONUP and self.focus:
            for component in self.components:
                if component.on_click(event.button):
                    return True
        return False

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
