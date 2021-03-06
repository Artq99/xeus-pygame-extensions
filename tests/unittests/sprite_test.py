from unittest import TestCase
from unittest.mock import Mock

from pygame.event import Event
from pygame import Rect, Surface, USEREVENT, MOUSEMOTION, MOUSEBUTTONUP
from pygame.sprite import Group

from xpgext.sprite import XPGESprite, SpriteBehaviour, ComponentNotFoundError

SPRITE_X = 0
SPRITE_Y = 0
SPRITE_SIZE_X = 100
SPRITE_SIZE_Y = 100
MOUSE_POS_INSIDE_SPRITE = (50, 50)
MOUSE_POS_OUTSIDE_SPRITE = (200, 200)
TEST_USEREVENT = Event(USEREVENT, dict())
TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE = Event(MOUSEMOTION, {'pos': MOUSE_POS_INSIDE_SPRITE})
TEST_MOUSEMOTION_EVENT_WITH_POS_OUTSIDE_SPRITE = Event(MOUSEMOTION, {'pos': MOUSE_POS_OUTSIDE_SPRITE})
TEST_MOUSEBUTTONUP_EVENT_WITH_POS_INSIDE_SPRITE = Event(MOUSEBUTTONUP, {'pos': MOUSE_POS_INSIDE_SPRITE, 'button': 0})


class TestComponent1(SpriteBehaviour):
    pass


class TestComponent2(SpriteBehaviour):
    pass


class TestComponent3(SpriteBehaviour):
    pass


class TestComponent4(SpriteBehaviour):
    pass


class XPGESpriteTest(TestCase):
    """Test class for XPGESprite class."""

    def setUp(self):
        self.sprite = XPGESprite(None)
        self.sprite.image = Surface((SPRITE_SIZE_X, SPRITE_SIZE_Y))
        self.sprite.position = (SPRITE_X, SPRITE_Y)

        self.component_1 = Mock(spec=TestComponent1)
        self.component_2 = Mock(spec=TestComponent2)
        self.component_3 = Mock(spec=TestComponent3)
        self.sprite.components.append(self.component_1)
        self.sprite.components.append(self.component_2)
        self.sprite.components.append(self.component_3)

    def test_should_add_sprite_to_group_on_creation(self):
        # given when
        group = Group()
        sprite = XPGESprite(None, group)

        # then
        self.assertTrue(group.has(sprite))
        self.assertEqual(0, sprite.groups().index(group))

    def test_should_add_sprite_to_two_groups_on_creation(self):
        # given when
        group1 = Group()
        group2 = Group()
        sprite = XPGESprite(None, group1, group2)

        # then
        self.assertTrue(group1.has(sprite))
        self.assertTrue(group2.has(sprite))
        self.assertEqual(0, sprite.groups().index(group1))
        self.assertEqual(1, sprite.groups().index(group2))

    def test_should_update_components(self):
        # when
        self.sprite.update()

        # then
        self.component_1.on_update.assert_called_once()
        self.component_2.on_update.assert_called_once()
        self.component_3.on_update.assert_called_once()

    def test_should_call_on_click_on_components(self):
        # given
        self.sprite._focus = True
        self.component_1.on_click = Mock(return_value=False)
        self.component_2.on_click = Mock(return_value=False)
        self.component_3.on_click = Mock(return_value=False)

        # when
        self.sprite.handle_event(TEST_MOUSEBUTTONUP_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        self.component_1.on_click.assert_called_once_with(0)
        self.component_2.on_click.assert_called_once_with(0)
        self.component_3.on_click.assert_called_once_with(0)

    def test_should_not_call_on_click_on_last_component(self):
        # given
        self.sprite._focus = True
        self.component_1.on_click = Mock(return_value=False)
        self.component_2.on_click = Mock(return_value=True)

        # when
        self.sprite.handle_event(TEST_MOUSEBUTTONUP_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        self.component_1.on_click.assert_called_once_with(0)
        self.component_2.on_click.assert_called_once_with(0)
        self.component_3.on_click.assert_not_called()

    def test_should_call_handle_event_on_components(self):
        # given
        self.component_1.on_handle_event = Mock(return_value=False)
        self.component_2.on_handle_event = Mock(return_value=False)
        self.component_3.on_handle_event = Mock(return_value=False)

        # when
        self.sprite.handle_event(TEST_USEREVENT)

        # then
        self.component_1.on_handle_event.assert_called_once_with(TEST_USEREVENT)
        self.component_2.on_handle_event.assert_called_once_with(TEST_USEREVENT)
        self.component_3.on_handle_event.assert_called_once_with(TEST_USEREVENT)

    def test_should_not_call_handle_event_on_last_component(self):
        # given
        self.component_1.on_handle_event = Mock(return_value=False)
        self.component_2.on_handle_event = Mock(return_value=True)

        # when
        self.sprite.handle_event(TEST_USEREVENT)

        # then
        self.component_1.on_handle_event.assert_called_once_with(TEST_USEREVENT)
        self.component_2.on_handle_event.assert_called_once_with(TEST_USEREVENT)
        self.component_3.on_handle_event.assert_not_called()

    def test_should_set_sprite_focus_to_true(self):
        # given
        self.sprite._rect = Mock(spec=Rect)
        self.sprite._rect.collidepoint = Mock(return_value=True)

        # when
        self.sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        x, y = MOUSE_POS_INSIDE_SPRITE
        self.sprite.rect.collidepoint.assert_called_once_with(x, y)
        self.assertTrue(self.sprite.focus)

    def test_should_set_sprite_focus_to_false(self):
        # given
        self.sprite._rect = Mock(spec=Rect)
        self.sprite._rect.collidepoint = Mock(return_value=False)

        # when
        self.sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        x, y = MOUSE_POS_INSIDE_SPRITE
        self.sprite.rect.collidepoint.assert_called_once_with(x, y)
        self.assertFalse(self.sprite.focus)

    def test_should_not_change_focus_when_take_focus_is_false(self):
        # given
        self.sprite.takes_focus = False
        self.sprite._rect = Mock(spec=Rect)

        # when
        self.sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        self.sprite.rect.collidepoint.assert_not_called()
        self.assertFalse(self.sprite.focus)

    def test_should_call_on_hover_on_components(self):
        # when
        self.sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_INSIDE_SPRITE)

        # then
        self.component_1.on_hover.assert_called_once()
        self.component_2.on_hover.assert_called_once()
        self.component_3.on_hover.assert_called_once()

    def test_should_call_on_hover_exit_on_components(self):
        # given
        self.sprite._focus = True

        # when
        self.sprite.handle_event(TEST_MOUSEMOTION_EVENT_WITH_POS_OUTSIDE_SPRITE)

        # then
        self.component_1.on_hover_exit.assert_called_once()
        self.component_2.on_hover_exit.assert_called_once()
        self.component_3.on_hover_exit.assert_called_once()

    def test_should_draw_sprite_onto_surface(self):
        # given
        surface = Mock(spec=Surface)

        # when
        self.sprite.draw(surface)

        # then
        surface.blit.assert_called_once_with(self.sprite.image, (SPRITE_X, SPRITE_Y))

    def test_should_get_component_by_type(self):
        # when
        component = self.sprite.get_component_by_type(TestComponent1)

        # then
        self.assertIsNotNone(component)
        self.assertEqual(self.component_1, component)

    def test_should_get_component_by_type_name(self):
        # when
        component = self.sprite.get_component_by_type_name("TestComponent1")

        # then
        self.assertIsNotNone(component)
        self.assertEqual(self.component_1, component)

    def test_should_raise_error_when_component_not_present(self):
        # when then
        with self.assertRaises(ComponentNotFoundError):
            self.sprite.get_component_by_type_name("TestComponent4")

    def test_should_raise_error_when_no_component_present(self):
        # given
        self.sprite.components.clear()

        # when then
        with self.assertRaises(ComponentNotFoundError):
            self.sprite.get_component_by_type_name("TestComponent1")

    def test_should_find_components_by_type(self):
        # given
        test_component = TestComponent1(self.sprite)
        self.sprite.components.append(test_component)

        # when
        components = self.sprite.find_components_by_type(TestComponent1)

        # then
        self.assertEqual(2, len(components))
        self.assertIn(self.component_1, components)
        self.assertIn(test_component, components)

    def test_should_find_components_by_type_name(self):
        # given
        test_component = TestComponent1(self.sprite)
        self.sprite.components.append(test_component)

        # when
        components = self.sprite.find_components_by_type_name("TestComponent1")

        # then
        self.assertEqual(2, len(components))
        self.assertIn(self.component_1, components)
        self.assertIn(test_component, components)

    def test_should_not_find_component_when_not_present(self):
        # when
        components = self.sprite.find_components_by_type_name("TestComponent4")

        # then
        self.assertEqual(0, len(components))

    def test_should_not_find_component_when_no_component_present(self):
        # given
        self.sprite.components.clear()

        # when
        components = self.sprite.find_components_by_type_name("TestComponent1")

        # then
        self.assertEqual(0, len(components))
