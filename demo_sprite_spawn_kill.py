import os

import pygame

from xpgext.application import XPGEApplication
from xpgext.scene import SimpleScene
from xpgext.scene_manager import SimpleSceneManager
from xpgext.sprite import XPGESprite, SpriteBehaviour


class Spawner(SpriteBehaviour):

    def __init__(self, sprite):
        super().__init__(sprite)
        self.star2 = pygame.image.load(os.path.join("demo_resources", "star2.png")).convert()

    def on_click(self, button):
        if button == 1:

            if len(self.scene_manager.find_by_name("spawned sprite")) != 0:
                print("Cannot spawn! The sprite already exists!")
                return None

            print("Spawning...")

            sprite = XPGESprite(self.scene_manager)
            sprite.image = self.star2
            sprite.name = "spawned sprite"
            sprite.position = (300, 10)
            sprite.components.append(Slave(sprite))

            self.scene_manager.spawn(sprite)

            print("Spawned!")


class Slave(SpriteBehaviour):

    def on_click(self, button):
        if button == 1:
            self.scene_manager.kill(self.sprite)

    def on_spawn(self):
        print("I'm alive!")

    def on_kill(self):
        print("I'm dying!")


class DemoScene(SimpleScene):

    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        star = pygame.image.load(os.path.join("demo_resources", "star.png")).convert()

        spawner_sprite = XPGESprite(self.scene_manager)
        spawner_sprite.image = star
        spawner_sprite.position = (10, 10)
        spawner_sprite.components.append(Spawner(spawner_sprite))
        self.sprites.append(spawner_sprite)


class Application(XPGEApplication):

    def __init__(self):
        super().__init__(SimpleSceneManager(), (640, 480))

        self.caption = "Demo: Spawning and killing sprites"

        self.scene_manager.register_scene(DemoScene, "demo")
        self.scene_manager.load_scene("demo")


if __name__ == "__main__":
    pygame.init()
    application = Application()
    application.run_main_loop()
    pygame.quit()
