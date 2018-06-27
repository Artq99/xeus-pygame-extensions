from unittest import TestCase
from unittest.mock import Mock

from pygame.event import Event
from pygame import Rect, USEREVENT, MOUSEMOTION

from xpgext.sprite import XPGESprite, XPGEGroup, SpriteBehaviour

MOUSE_POS = (50, 50)
TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE = Event(MOUSEMOTION, {'pos': (50, 50)})
TEST_MOUSEMOTION_EVENT_WITH_POS_OUTSIDE_SPRITE = Event(MOUSEMOTION, {'pos': (200, 200)})


class XPGESpriteTest(TestCase):
    """Test class for XPGESprite class."""

    def test_should_add_sprite_to_group_on_creation(self):
        # given when
        group = XPGEGroup()
        sprite = XPGESprite(None, group)

        # then
        self.assertTrue(group.has(sprite))
        self.assertEqual(0, sprite.groups().index(group))

    def test_should_add_sprite_to_two_groups_on_creation(self):
        # given when
        group1 = XPGEGroup()
        group2 = XPGEGroup()
        sprite = XPGESprite(None, group1, group2)

        # then
        self.assertTrue(group1.has(sprite))
        self.assertTrue(group2.has(sprite))
        self.assertEqual(0, sprite.groups().index(group1))
        self.assertEqual(1, sprite.groups().index(group2))

    def test_should_update_single_component(self):
        # given
        component_mock = Mock(spec=SpriteBehaviour)
        sprite = XPGESprite(None)
        sprite.components.append(component_mock)

        # when
        sprite.update()

        # then
        component_mock.on_update.assert_called_once()

    def test_should_update_many_component(self):
        # given
        component_mock_1 = Mock(spec=SpriteBehaviour)
        component_mock_2 = Mock(spec=SpriteBehaviour)
        component_mock_3 = Mock(spec=SpriteBehaviour)

        sprite = XPGESprite(None)
        sprite.components.append(component_mock_1)
        sprite.components.append(component_mock_2)
        sprite.components.append(component_mock_3)

        # when
        sprite.update()

        # then
        component_mock_1.on_update.assert_called_once()
        component_mock_2.on_update.assert_called_once()
        component_mock_3.on_update.assert_called_once()

    def test_should_call_handle_event_on_single_component(self):
        # given
        event = Event(USEREVENT, dict())
        component = Mock(spec=SpriteBehaviour)
        sprite = XPGESprite(None)
        sprite.components.append(component)

        # when
        sprite.handle_event(event)

        # then
        component.on_handle_event.assert_called_once_with(event)

    def test_should_call_handle_event_on_many_components(self):
        # given
        event = Event(USEREVENT, dict())
        component_mock_1 = Mock(spec=SpriteBehaviour)
        component_mock_2 = Mock(spec=SpriteBehaviour)
        component_mock_3 = Mock(spec=SpriteBehaviour)

        sprite = XPGESprite(None)
        sprite.components.append(component_mock_1)
        sprite.components.append(component_mock_2)
        sprite.components.append(component_mock_3)

        # when
        sprite.handle_event(event)

        # then
        component_mock_1.on_handle_event.assert_called_once_with(event)
        component_mock_2.on_handle_event.assert_called_once_with(event)
        component_mock_3.on_handle_event.assert_called_once_with(event)

    def test_should_set_sprite_focus_to_true(self):
        # given
        sprite = XPGESprite(None)
        sprite.rect = Mock(spec=Rect)
        sprite.rect.collidepoint = Mock(return_value=True)

        # when
        sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        sprite.rect.collidepoint.assert_called_once_with(MOUSE_POS)
        self.assertTrue(sprite.focus)

    def test_should_set_sprite_focus_to_false(self):
        # given
        sprite = XPGESprite(None)
        sprite.rect = Mock(spec=Rect)
        sprite.rect.collidepoint = Mock(return_value=False)

        # when
        sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        sprite.rect.collidepoint.assert_called_once_with(MOUSE_POS)
        self.assertFalse(sprite.focus)

    def test_should_not_change_focus_when_take_focus_is_false(self):
        # given
        sprite = XPGESprite(None)
        sprite.take_focus = False
        sprite.rect = Mock(spec=Rect)

        mouse_pos = (50, 50)
        event = Event(MOUSEMOTION, {'pos': mouse_pos})

        # when
        sprite.handle_event(event)

        # then
        sprite.rect.collidepoint.assert_not_called()
        self.assertFalse(sprite.focus)

    def test_should_call_on_hover_on_components(self):
        # given
        sprite = XPGESprite(None)
        sprite.rect = Rect(0, 0, 100, 100)
        component_1 = Mock(spec=SpriteBehaviour)
        component_2 = Mock(spec=SpriteBehaviour)
        component_3 = Mock(spec=SpriteBehaviour)
        sprite.components.append(component_1)
        sprite.components.append(component_2)
        sprite.components.append(component_3)

        # when
        sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        component_1.on_hover.assert_called_once()
        component_2.on_hover.assert_called_once()
        component_3.on_hover.assert_called_once()

    def test_should_call_on_hover_exit_on_components(self):
        # given
        sprite = XPGESprite(None)
        sprite.rect = Rect(0, 0, 100, 100)
        sprite.focus = True
        component_1 = Mock(spec=SpriteBehaviour)
        component_2 = Mock(spec=SpriteBehaviour)
        component_3 = Mock(spec=SpriteBehaviour)
        sprite.components.append(component_1)
        sprite.components.append(component_2)
        sprite.components.append(component_3)

        # when
        sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_OUTSIDE_SPRITE)

        # then
        component_1.on_hover_exit.assert_called_once()
        component_2.on_hover_exit.assert_called_once()
        component_3.on_hover_exit.assert_called_once()

    def test_should_draw_sprite_onto_surface(self):
        pass

