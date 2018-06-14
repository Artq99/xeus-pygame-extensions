from unittest import TestCase

from xpgext.scene_manager import SimpleSceneManager
from xpgext.scene import SimpleScene


class SimpleSceneManagerTest(TestCase):
    """Test class for SimpleSceneManager class."""

    def test_should_create_instance(self):
        # given when
        simple_scene_manager = SimpleSceneManager()

        # then
        self.assertIsNotNone(simple_scene_manager)

    def test_should_register_scene(self):
        simple_scene_manager = SimpleSceneManager()
        test_scene_name = 'test scene'
        test_scene = SimpleScene(simple_scene_manager)

        simple_scene_manager.register_scene(test_scene, test_scene_name)

        self.assertIn(test_scene, simple_scene_manager._scenes.values())
        self.assertIn(test_scene_name, simple_scene_manager._scenes.keys())
