import pygame
from pygame.locals import *


class XPGESprite(pygame.sprite.Sprite):
    """
    Base class for all the visible game elements.
    """

    def __init__(self, scene_manager, *groups):
        super().__init__(*groups)

        self._previous_focus = False

        self._scene_manager = scene_manager
        self._image = None
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._is_active = True
        self._takes_focus = True
        self._components = list()
        self._focus = False
        self._name = None

    @property
    def scene_manager(self):
        """
        The scene manager that governs the sprite, given on initialisation.

        The sprite has a reference to the scene manager, so it has the access to all the information about the scene,
        and, thus, to all the other sprites. This way it can interact with them or cause the scene manager to make
        certain actions not directly related to any sprite, like, for example, opening a UI window.
        """

        return self._scene_manager

    @property
    def image(self):
        """
        The image of the sprite.

        The instance of pygame.Surface assigned to this property will be the image representing this sprite object
        on the screen. What is more, on assignment, the width and height property of the rect of the sprite will be
        adjusted to the size of the new surface.
        """

        return self._image

    @image.setter
    def image(self, surface):
        self._image = surface
        self._rect.width = self._image.get_rect().width
        self._rect.height = self._image.get_rect().height

    @property
    def rect(self):
        """
        The rectangle of the sprite.

        The instance of pygame.Rect holding information about the position and the size of the sprite.
        """

        return self._rect

    @property
    def is_active(self):
        """
        Status of the sprite.

        Sprite can exist in the scene, but when this property is set to False, it is not being rendered,
        and it does not react to any input. It is a convenient way to 'turn off' the sprite without loosing its
        settings.
        """

        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def takes_focus(self):
        """The property determining whether the sprite can be targeted by the mouse cursor."""

        return self._takes_focus

    @takes_focus.setter
    def takes_focus(self, value):
        self._takes_focus = value

    @property
    def components(self):
        """
        The components of the sprite.

        These are the descendants of the class SpriteBehaviour that control all the actions of the sprite.
        """

        return self._components

    @property
    def focus(self):
        """
        Is mouse cursor over the sprite?

        This read-only property returns True when the coordinates of the mouse cursor collide with the rectangle
        of the sprite.
        """

        return self._focus

    @property
    def name(self):
        """
        The name of the sprite.

        This string is a custom name that can be later used to search for the sprite by the methods find_by_name
        and get_by_name in the scene manager.
        """

        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def position(self):
        """
        The position of the sprite on the screen.

        This property is a shortcut for operating on the property topleft of the rectangle of the sprite.
        """

        return self._rect.topleft

    @position.setter
    def position(self, new_position):
        self._rect.topleft = new_position

    def update(self):
        """
        Update sprite and call on_update methods from each of its components.
        """

        if self._is_active:
            for component in self._components:
                component.on_update()

    def handle_event(self, event):
        """
        Handle the given event. It is passed to each of its components

        :param event: event
        :type event: pygame.event.Event
        """

        if not self._is_active:
            return False
        self._handle_mouse_motion(event)
        handled = self._handle_mouse_button_up(event)
        if not handled:
            for component in self._components:
                if component.on_handle_event(event):
                    handled = True
                    break
        return handled

    def _handle_mouse_motion(self, event):
        if event.type == MOUSEMOTION and self._takes_focus:
            self._previous_focus = self._focus
            self._focus = self._rect.collidepoint(event.pos[0], event.pos[1])
            self._handle_hover()

    def _handle_hover(self):
        if self._focus is self._previous_focus:
            return None
        for component in self._components:
            if self._focus:
                component.on_hover()
            else:
                component.on_hover_exit()

    def _handle_mouse_button_up(self, event):
        handled = False
        if event.type == MOUSEBUTTONUP and self._focus:
            for component in self._components:
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

        if self._is_active:
            surface.blit(self._image, self._rect.topleft)

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
        if self._name == name:
            result.append(self)
        return result


class SpriteBehaviour:
    """
    Base class for scripts controlling sprite behaviour.

    Override the appropriate method and add the instance to sprite.components list.
    """

    def __init__(self, sprite):
        self._sprite = sprite

    @property
    def sprite(self):
        """The sprite to which the script belongs."""

        return self._sprite

    @property
    def scene_manager(self):
        """
        Alias for SpriteBehaviour.sprite.scene_manager.

        This property provides easier access to the scene manager.
        """
        
        return self.sprite.scene_manager

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
