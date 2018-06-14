from unittest import TestCase
from unittest.mock import Mock, MagicMock

from pygame import Surface
from pygame.event import Event

from xpgext.scene_manager import SimpleSceneManager, SceneLoadingError
from xpgext.scene import SimpleScene
from xpgext.sprite import XPGESprite, SpriteBehaviour


class SimpleSceneManagerTest(TestCase):
    """Test class for SimpleSceneManager class."""

    def test_should_create_instance(self):
        # given when
        simple_scene_manager = SimpleSceneManager()

        # then
        self.assertIsNotNone(simple_scene_manager)

    def test_should_register_scene(self):
        # given
        simple_scene_manager = SimpleSceneManager()
        test_scene_name = 'test scene'
        test_scene = SimpleScene(simple_scene_manager)

        # when
        simple_scene_manager.register_scene(test_scene, test_scene_name)

        # then
        self.assertIn(test_scene, simple_scene_manager._scenes.values())
        self.assertIn(test_scene_name, simple_scene_manager._scenes.keys())

    def test_should_load_scene(self):
        # given
        simple_scene_manager = SimpleSceneManager()
        simple_scene_manager._sprites = MagicMock()

        test_sprite = XPGESprite(simple_scene_manager)
        component_mock = Mock(spec=SpriteBehaviour)
        test_sprite.components.append(component_mock)
        sprite_list = [test_sprite]

        simple_scene_manager._sprites.__iter__ = Mock(return_value=iter(sprite_list))
        test_scene_name = 'test name'

        class TestSimpleScene(SimpleScene):

            def __init__(self, scene_manager):
                super().__init__(scene_manager)
                self.sprites = sprite_list

        simple_scene_manager.register_scene(TestSimpleScene, test_scene_name)

        # when
        simple_scene_manager.load_scene(test_scene_name)

        # then
        self.assertIsInstance(simple_scene_manager._current_scene, TestSimpleScene)
        simple_scene_manager._sprites.clear.assert_called_once()
        simple_scene_manager._sprites.append.assert_called_once_with(test_sprite)
        component_mock.on_scene_loaded.assert_called_once()

    def test_should_not_load_scene_when_not_registered(self):
        # given
        simple_scene_manager = SimpleSceneManager()

        # when then
        with self.assertRaises(SceneLoadingError):
            simple_scene_manager.load_scene('test scene')

    def test_should_draw_scene(self):
        # given
        simple_scene_manager = SimpleSceneManager()
        test_sprite_1 = Mock(spec=XPGESprite)
        test_sprite_2 = Mock(spec=XPGESprite)
        test_sprite_3 = Mock(spec=XPGESprite)
        sprite_list = [test_sprite_1, test_sprite_2, test_sprite_3]
        simple_scene_manager._sprites = sprite_list
        surface = Mock(spec=Surface)

        # when
        simple_scene_manager.draw(surface)

        # then
        surface.fill.assert_called_once_with((0, 0, 0))
        test_sprite_1.draw.assert_called_once_with(surface)
        test_sprite_2.draw.assert_called_once_with(surface)
        test_sprite_3.draw.assert_called_once_with(surface)

    def test_should_handle_event(self):
        # given
        simple_scene_manager = SimpleSceneManager()
        test_sprite_1 = Mock(spec=XPGESprite)
        test_sprite_1.handle_event = Mock(return_value=False)
        test_sprite_2 = Mock(spec=XPGESprite)
        test_sprite_2.handle_event = Mock(return_value=False)
        test_sprite_3 = Mock(spec=XPGESprite)
        test_sprite_3.handle_event = Mock(return_value=False)
        sprite_list = [test_sprite_1, test_sprite_2, test_sprite_3]
        simple_scene_manager._sprites = sprite_list
        event = Mock(spec=Event)

        # when
        simple_scene_manager.handle_event(event)

        # then
        test_sprite_1.handle_event.assert_called_once_with(event)
        test_sprite_2.handle_event.assert_called_once_with(event)
        test_sprite_3.handle_event.assert_called_once_with(event)

    def test_should_stop_iteration_while_handling_event(self):
        # given
        simple_scene_manager = SimpleSceneManager()
        test_sprite_1 = Mock(spec=XPGESprite)
        test_sprite_1.handle_event = Mock(return_value=False)
        test_sprite_2 = Mock(spec=XPGESprite)
        test_sprite_2.handle_event = Mock(return_value=True)
        test_sprite_3 = Mock(spec=XPGESprite)
        test_sprite_3.handle_event = Mock(return_value=False)
        sprite_list = [test_sprite_1, test_sprite_2, test_sprite_3]
        simple_scene_manager._sprites = sprite_list
        event = Mock(spec=Event)

        # when
        simple_scene_manager.handle_event(event)

        # then
        test_sprite_1.handle_event.assert_not_called()
        test_sprite_2.handle_event.assert_called_once_with(event)
        test_sprite_3.handle_event.assert_called_once_with(event)

    def test_should_update(self):
        # given
        simple_scene_manager = SimpleSceneManager()
        test_sprite_1 = Mock(spec=XPGESprite)
        test_sprite_2 = Mock(spec=XPGESprite)
        test_sprite_3 = Mock(spec=XPGESprite)
        sprite_list = [test_sprite_1, test_sprite_2, test_sprite_3]
        simple_scene_manager._sprites = sprite_list

        # when
        simple_scene_manager.update()

        # then
        test_sprite_1.update.assert_called_once()
        test_sprite_2.update.assert_called_once()
        test_sprite_3.update.assert_called_once()
