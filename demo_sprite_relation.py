import os

from xpgext.application import XPGApplication
from xpgext.scene_manager import SimpleSceneManager
from xpgext.scene import SimpleScene
from xpgext.sprite import Sprite, SpriteBehaviour


class ToggleSprite(SpriteBehaviour):

    def __init__(self, sprite):
        super().__init__(sprite)
        self.sprite_to_toggle = None

    def on_scene_loaded(self):
        self.sprite_to_toggle = self.sprite.scene_manager.get_by_name('sprite2')

    def on_click(self, button):
        self.sprite_to_toggle.active = not self.sprite_to_toggle.active


class DemoScene(SimpleScene):

    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        sprite1 = Sprite(self.scene_manager)
        sprite1.load_image(os.path.join('demo_resources', 'star.png'))
        sprite1.set_pos(10, 10)
        sprite1.components.append(ToggleSprite(sprite1))

        sprite2 = Sprite(self.scene_manager)
        sprite2.name = 'sprite2'
        sprite2.load_image(os.path.join('demo_resources', 'star2.png'))
        sprite2.set_pos(200, 10)

        self.sprites.append(sprite1)
        self.sprites.append(sprite2)


class Application(XPGApplication):

    def __init__(self):
        super().__init__(SimpleSceneManager(), (640, 480))
        self.scene_manager.register_scene(DemoScene, 'demo')
        self.scene_manager.load_scene('demo')


if __name__ == '__main__':
    application = Application()
    application.run_main_loop()
