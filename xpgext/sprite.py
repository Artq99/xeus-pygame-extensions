import pygame


class Sprite(pygame.sprite.Sprite):

    def __init__(self, scene_manager, *groups):
        super().__init__(groups)
        self.scene_manager = scene_manager
        self.image = None
        self.rect = None

    def load_image(self, path):
        """
        Load image from the given path.

        :param path: path to an image file
        :type path: str
        """

        self.image = pygame.image.load(path).convert()
        self.rect = self.image.get_rect()

    def handle_event(self, event):
        return False

    def draw(self, surface):
        """
        Draw the sprite onto the given surface.

        :param surface: the destination surface
        :type surface: pygame.Surface
        """

        surface.blit(self.image, self.rect.topleft)

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)


class SpriteBehaviour:
    """
    Base class for scripts controlling sprite behaviour.

    Override the appropriate method and instantiate the descendant of this class
    to Sprite.behaviourScript.
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
