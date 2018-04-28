from unittest import TestCase

from xpgext.sprite import XPGESprite, XPGEGroup


class SpriteGroupRelationTest(TestCase):
    """Test class validating the functioning of the relation between sprites and groups."""

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
