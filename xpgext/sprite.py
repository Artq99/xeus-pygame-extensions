import pygame
from pygame.locals import *


class XPGESprite(pygame.sprite.Sprite):
    """
    Base class for all the visible game elements.
    """

    def __init__(self, scene_manager, *groups):
        super().__init__(*groups)
        self.image = None
        self.rect = None
        self.active = True
        self.take_focus = True
        self.interacts_with_mouse = True
        self.components = list()

        self._previous_focus = False
        self.focus = False

        self.name = None

        self._scene_manager = scene_manager

    @property
    def scene_manager(self):
        """
        Get the scene manager that governs this sprite.

        :return: scene manager instance
        :rtype: SimpleSceneManager
        """

        return self._scene_manager

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
                    break
        return handled

    def _handle_mouse_motion(self, event):
        if event.type == MOUSEMOTION and self.take_focus:
            self._previous_focus = self.focus
            self.focus = self.rect.collidepoint(event.pos)
            self._handle_hover()

    def _handle_hover(self):
        if self.focus is self._previous_focus:
            return None
        for component in self.components:
            if self.focus:
                component.on_hover()
            else:
                component.on_hover_exit()

    def _handle_mouse_button_up(self, event):
        handled = False
        if event.type == MOUSEBUTTONUP and self.focus:
            for component in self.components:
                if component.on_click(event.button):
                    handled = True
                    break
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

    def find_by_name(self, name):
        """
        This function is not intended to be used on its own.

        Returns a list containing this instance if its name matches the given one.

        :param name: name to check
        :type name: str
        :return: list of elements
        :rtype: list
        """

        result = list()
        if self.name == name:
            result.append(self)
        return result


class SpriteBehaviour:
    """
    Base class for scripts controlling sprite behaviour.

    Override the appropriate method and add the instance to sprite.components list.
    """

    def __init__(self, sprite):
        self.sprite = sprite

    def on_scene_loaded(self):
        """
        Method called when the scene has been loaded.

        It is intended to use to initialize all the behaviour variables, that can be dependent on other scene elements,
        that could be unavailable when __init__ method is called. Script attributes can be declared here, since it is
        the first method called after initialization, however, the convention is to create them in __init__ method
        and initialize them here later on.
        """

    def on_update(self):
        """Method called on Sprite.update."""

    def on_handle_event(self, event):
        """
        Method called on Sprite.handle_event.

        It is advised not to use this method to handle on_click, on_hover and on_hover_exit. Override the corresponding
        methods instead. This method may return True if you wish the game manager to stop checking if any sprite handled
        the given event after this call.
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


class XPGEGroup(pygame.sprite.Group):
    """Group implementation adjusted to work with XPGE Sprite."""

    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.name = None

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
        Call the update method of every sprite member in reversed order.

        Overrides the default implementation from pygame.sprite.Group.
        """

        for sprite in reversed(self.sprites()):
            sprite.update(*args)

    def draw(self, surface):
        """
        Draw all the member sprites onto the surface.

        The method calls the draw method of each member XPGESprite.

        Overrides the default implementation from pygame.sprite.Group.

        :param surface: the pygame main surface
        :type surface: pygame.Surface
        """

        for sprite in reversed(self.sprites()):
            sprite.draw(surface)

    def find_by_name(self, name):
        """
        Find elements of the given name.

        Returns a list containing this Group instance if its name matches the given one and all the containing sprites
        whose name matches the given one.

        :param name: the name of elements to find
        :type name: str
        :return: list of elements
        :rtype: list
        """

        result = list()
        if self.name == name:
            result.append(self)
        for sprite in self.sprites():
            if sprite.name == name:
                result.append(sprite)
        return result
