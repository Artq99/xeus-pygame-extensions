from unittest import TestCase
from unittest.mock import Mock

import pygame

from tests.test_utils import run_with_timeout
from xpgext.application import XPGEApplication
from xpgext.scene_manager import SimpleSceneManager


class XPGApplicationTest(TestCase):
    """The test class for the embedded tests of the application module."""

    def setUp(self):
        pygame.init()
        self.scene_manager_mock = Mock(spec=SimpleSceneManager)

    def tearDown(self):
        pygame.quit()

    def test_should_create_application_object(self):
        # when
        application = XPGEApplication(self.scene_manager_mock, (800, 600))

        # then
        self.assertIsNotNone(application)

    def test_should_run_main_loop(self):
        # given
        application = XPGEApplication(self.scene_manager_mock, (800, 600))

        # when
        run_with_timeout(1, application.run_main_loop)

        # then
        self.assertTrue(application.is_running)
        self.scene_manager_mock.update.assert_called()
