from unittest import TestCase
from unittest.mock import Mock

import pygame

from xpgext.application import XPGApplication
from xpgext.scene_manager import SimpleSceneManager

from tests.test_utils import run_with_timeout


class XPGApplicationTest(TestCase):
    """Test class for XPGApplication."""

    def setUp(self):
        pygame.init()
        self.scene_manager_mock = Mock(spec=SimpleSceneManager)

    def tearDown(self):
        pygame.quit()

    def test_should_create_application_object(self):
        # when
        application = XPGApplication(self.scene_manager_mock, (800, 600))

        # then
        self.assertIsNotNone(application)

    def test_should_run_main_loop(self):
        # given
        application = XPGApplication(self.scene_manager_mock, (800, 600))

        # when
        run_with_timeout(1, application.run_main_loop)

        # then
        self.assertTrue(application.is_running)
        self.scene_manager_mock.update.assert_called()
