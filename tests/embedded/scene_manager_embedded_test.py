from unittest import TestCase

import pygame
from pygame import Rect

from xpgext.scene_manager import SimpleSceneManager


class SimpleSceneManagerTest(TestCase):
    """The test class for the embedded tests of the scene_manager module."""

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_should_return_screen_rect(self):
        # given
        simple_scene_manager = SimpleSceneManager()

        # when
        screen_rect = simple_scene_manager.screen_rect

        # then
        self.assertIsNotNone(screen_rect)
        self.assertIsInstance(screen_rect, Rect)
        self.assertEqual(0, screen_rect.top)
        self.assertEqual(0, screen_rect.left)
        self.assertEqual(600, screen_rect.bottom)
        self.assertEqual(800, screen_rect.right)
