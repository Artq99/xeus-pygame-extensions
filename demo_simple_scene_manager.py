import os

import pygame

from xpgext.application import XPGApplication
from xpgext.scene_manager import SimpleSceneManager
from xpgext.scene import SimpleScene
from xpgext.sprite import XPGESprite


class DemoScene(SimpleScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        star = pygame.image.load(os.path.join("demo_resources", "star.png")).convert()

        demo_sprite = XPGESprite(self.scene_manager)
        demo_sprite.image = star
        demo_sprite.position = (270, 190)
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
