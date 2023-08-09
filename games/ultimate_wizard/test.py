import unittest

from board import Board

class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_get_field_enemy(self):
        field_content = self.board.get_field(self.board.enemies[0].x, self.board.enemies[0].y)
        self.assertListEqual(field_content, ['enemy'])

    def test_get_field_player_plaftorm(self):
        field_content = self.board.get_field(self.board.player.x, self.board.player.y)
        self.assertListEqual(field_content, ['player', 'platform'])

    def test_get_field_empty(self):
        #assert that enemy does not have platform beneath its feet
        enemy = self.board.enemies[0]
        below_enemy_x = enemy.x
        below_enemy_y = enemy.y + 1

        field_content = self.board.get_field(below_enemy_x, below_enemy_y)
        self.assertListEqual(field_content, [])

    def test_no_platform_below_enemy(self):
        enemy = self.board.enemies[0]

        self.assertFalse(self.board.has_platform_below(enemy.x, enemy.y))

    def test_free_fall(self):
        field_content = self.board.get_field(9, 3)
        self.assertListEqual(field_content, ['enemy'])

        field_content = self.board.get_field(9, 5)
        self.assertListEqual(field_content, ['platform'])

        for _ in range(10):
            self.board.free_fall(self.board.enemy) #in 3rd iteration it should hit platform and not move anymore

        field_content = self.board.get_field(9, 5)

        expected = ['platform', 'enemy']
        actual = field_content

        for item in expected:
            if item in actual:
                actual.remove(item)

        self.assertListEqual(actual, [])        


if __name__ == '__main__':
    unittest.main()
    