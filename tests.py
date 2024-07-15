import unittest
from maze import Maze
from graphics import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 10
        num_cols = 12
        m1 = Maze(0,0,num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells), num_rows
        )
        self.assertEqual(
            len(m1._cells[0]), num_cols
        )
        

    def test_maze_create_cells_large(self):
        num_rows = 12
        num_cols = 16
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )
        
    def test_break_entrance_and_exit(self):
        num_rows = 10
        num_cols = 12
        win = Window(800, 600)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(m1._cells[0][0].has_top_wall, False)
        self.assertEqual(m1._cells[9][11].has_bottom_wall, False)
        
    def test_reset_cells_visited(self):
        num_rows = 12
        num_cols = 16
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        for i in range(num_rows):
            for j in range(num_cols):
                self.assertEqual(m1._cells[i][j].visited, False)
        
        
if __name__ == "__main__":
    unittest.main()