import os

import pygame
from pygame.locals import *

from xpgext.application import XPGEApplication
from xpgext.scene import SimpleScene
from xpgext.scene_manager import SimpleSceneManager
from xpgext.sprite import XPGESprite, SpriteBehaviour


class DemoSpriteBehaviour(SpriteBehaviour):

    def __init__(self, sprite):
        super().__init__(sprite)
        self.counter = 0
        self.default_image = None
        self.another_image = None

    def on_scene_loaded(self):
        self.default_image = self.sprite.image
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

    def on_spawn(self):
        print("Sprite spawned!")


class DemoScene(SimpleScene):

    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        star = pygame.image.load(os.path.join("demo_resources", "star.png")).convert()

        demo_sprite = XPGESprite(self.scene_manager)
        demo_sprite.image = star
        demo_sprite.position = (270, 190)
        demo_sprite.components.append(DemoSpriteBehaviour(demo_sprite))
        self.sprites.append(demo_sprite)


class Application(XPGEApplication):

    def __init__(self):
        super().__init__(SimpleSceneManager(), (640, 480))

        self.caption = "Demo: SpriteBehaviour usage"

        self.scene_manager.register_scene(DemoScene, "demo")
        self.scene_manager.load_scene("demo")


if __name__ == "__main__":
    pygame.init()
    application = Application()
    application.run_main_loop()
    pygame.quit()
