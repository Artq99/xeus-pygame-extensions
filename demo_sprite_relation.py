import os

import pygame

from xpgext.application import XPGEApplication
from xpgext.scene import SimpleScene
from xpgext.scene_manager import SimpleSceneManager
from xpgext.sprite import XPGESprite, SpriteBehaviour


class ToggleSprite(SpriteBehaviour):

    def __init__(self, sprite):
        super().__init__(sprite)

        self.sprite_to_toggle = None

    def on_scene_loaded(self):
        self.sprite_to_toggle = self.sprite.scene_manager.get_by_name("sprite2")

    def on_click(self, button):
        self.sprite_to_toggle.is_active = not self.sprite_to_toggle.is_active


class DemoScene(SimpleScene):

    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        star1 = pygame.image.load(os.path.join("demo_resources", "star.png")).convert()
        star2 = pygame.image.load(os.path.join("demo_resources", "star2.png")).convert()

        sprite1 = XPGESprite(self.scene_manager)
        sprite1.image = star1
        sprite1.position = (10, 10)
        sprite1.components.append(ToggleSprite(sprite1))

        sprite2 = XPGESprite(self.scene_manager)
        sprite2.name = "sprite2"
        sprite2.image = star2
        sprite2.position = (200, 10)

        self.sprites.append(sprite1)
        self.sprites.append(sprite2)


class Application(XPGEApplication):

    def __init__(self):
        super().__init__(SimpleSceneManager(), (640, 480))

        self.caption = "Demo: Sprite relation"

        self.scene_manager.register_scene(DemoScene, "demo")
        self.scene_manager.load_scene("demo")


if __name__ == '__main__':
    pygame.init()
    application = Application()
    application.run_main_loop()
    pygame.quit()
