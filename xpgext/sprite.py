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
