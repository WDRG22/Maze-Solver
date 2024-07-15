from cell import Cell
import random
import time

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.x1 = x1    
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self.sleep = 0
        self._cells = []
        if seed: 
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    
    def _create_cells(self):
        self._cells = [[Cell(self._win) for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        cell = self._cells[i][j]
        cell_x1 = self.x1 + (self.cell_size_x * j)
        cell_x2 = cell_x1 + self.cell_size_x
        cell_y1 = self.y1 + (self.cell_size_y * i)
        cell_y2 = cell_y1 + self.cell_size_y      
        cell.draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()
        
    def _animate(self):
        self._win.redraw()
        time.sleep(self.sleep)
        
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            
            # Check cell above
            if i > 0:
                if not self._cells[i - 1][j].visited:
                    to_visit.append((i - 1, j))
            # Check cell below
            if i < self.num_rows - 1:
                if not self._cells[i + 1][j].visited:
                    to_visit.append((i + 1, j))
            # Check cell to the left
            if j > 0:
                if not self._cells[i][j - 1].visited:
                    to_visit.append((i, j - 1))
            # Check cell to the right
            if j < self.num_cols - 1:
                if not self._cells[i][j + 1].visited:
                    to_visit.append((i, j + 1))
            
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            next_cell = to_visit[random.randrange(len(to_visit))]
            
            # knock out walls between this cell and the next cell(s)
            # right
            if next_cell[0] == i and next_cell[1] == j + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False
            # left
            elif next_cell[0] == i and next_cell[1] == j - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
            # down
            elif next_cell[0] == i + 1 and next_cell[1] == j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
            # up
            elif next_cell[0] == i - 1 and next_cell[1] == j:
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
            
            self._break_walls_r(next_cell[0], next_cell[1])
        
    def _break_entrance_and_exit(self):
        if self._win is None:
            return
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False
                
                
    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        self.sleep = 0.025

        # Check if we have reached the bottom-right corner (goal)
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        
        # Move up
        if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_top_wall:
                self._cells[i][j].draw_move(self._cells[i-1][j])
                good_move = self._solve_r(i - 1, j)
                if not good_move:
                    self.sleep = 0.1
                    self._cells[i][j].draw_move(self._cells[i-1][j], undo=True)
                else:
                    return True
        
        # Move right
        if i < self.num_rows - 1 and not self._cells[i + 1][j].visited and not self._cells[i][j].has_bottom_wall:
                self._cells[i][j].draw_move(self._cells[i + 1][j])
                good_move = self._solve_r(i + 1, j)
                if not good_move:
                    self.sleep = 0.1
                    self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)
                else:
                    return True

        # Move left
        if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j].has_left_wall:
                self._cells[i][j].draw_move(self._cells[i][j - 1])
                good_move = self._solve_r(i, j - 1)
                if not good_move:
                    self.sleep = 0.1
                    self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)
                else:
                    return True

        # Move right
        if j < self.num_cols - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j].has_right_wall:
                self._cells[i][j].draw_move(self._cells[i][j + 1])
                good_move = self._solve_r(i, j + 1)
                if not good_move:
                    self.sleep = 0.1
                    self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)
                else:
                    return True

        # No possible moves from here
        return False