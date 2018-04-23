import os

import pygame
from pygame.locals import *

from xpgext.application import XPGApplication
from xpgext.scene_manager import SimpleSceneManager
from xpgext.scene import SimpleScene
from xpgext.sprite import Sprite, SpriteBehaviour


class DemoSpriteBehaviour(SpriteBehaviour):

    def __init__(self, sprite):
        super().__init__(sprite)

        self.counter = 0
        self.default_image = sprite.image
        self.another_image = pygame.image.load(os.path.join('demo_resources', 'star2.png'))

    def on_update(self):
        self.counter += 1
        if self.counter % 100 == 0:
            print("Sprite update {}!".format(self.counter))

    def on_handle_event(self, event):
        if event.type == MOUSEMOTION:
            print("Mouse moved! {}".format(event.rel))

    def on_click(self, button):
        print("Mouse button {} clicked!".format(button))

    def on_hover(self):
        self.sprite.image = self.another_image

    def on_hover_exit(self):
        self.sprite.image = self.default_image


class DemoScene(SimpleScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        demo_sprite = Sprite(self.scene_manager)
        demo_sprite.load_image(os.path.join("demo_resources", "star.png"))
        demo_sprite.set_pos(270, 190)
        demo_sprite.behaviour = DemoSpriteBehaviour(demo_sprite)
        self.sprites.append(demo_sprite)


class Application(XPGApplication):
    def __init__(self):
        super().__init__(SimpleSceneManager(), (640, 480))
        self.scene_manager.register_scene(DemoScene, "demo")
        self.scene_manager.load_scene("demo")


if __name__ == "__main__":
    pygame.init()
    application = Application()
    application.run_main_loop()
    pygame.quit()