import unittest

from board import Board

class BoardTest(unittest.TestCase):
    
    def setUp(self):
        self.board = Board()
    
    def test_get_field_enemy(self):
        field_content = self.board.get_field(self.board.enemy.x, self.board.enemy.y)
        self.assertListEqual(field_content, ['enemy'])
        
    def test_get_field_player_plaftorm(self):
        field_content = self.board.get_field(self.board.player.x, self.board.player.y)
        self.assertListEqual(field_content, ['player', 'platform'])
        
    def test_get_field_empty(self):
        #assert that enemy does not have platform beneath its feet
        below_enemy_x = self.board.enemy.x
        below_enemy_y = self.board.enemy.y + 1
        
        field_content = self.board.get_field(below_enemy_x, below_enemy_y)
        self.assertListEqual(field_content, [])

    def test_no_platform_below_enemy(self):
        enemy_x = self.board.enemy.x
        enemy_y = self.board.enemy.y
        
        self.assertFalse(self.board.has_platform_below(enemy_x, enemy_y))

    def test_free_fall(self):
        field_content = self.board.get_field(9, 3)
        self.assertListEqual(field_content, ['enemy'])
        
        field_content = self.board.get_field(9, 5)
        self.assertListEqual(field_content, ['platform'])
        
        for _ in range(10):
            self.board.free_fall(self.board.enemy) #in 3rd iteration it should hit platform and not move anymore
        
        field_content = self.board.get_field(9, 5)
        self.assertListEqual(field_content, ['platform', 'enemy'])   
        

if __name__ == '__main__':
    unittest.main()
    