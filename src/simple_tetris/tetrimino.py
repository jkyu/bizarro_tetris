from simple_tetris.grid import Grid
from simple_tetris.row import Row
from abc import ABC, abstractmethod

class Tetrimino(ABC):

    def __init__(self, left_column):
        self.left_column = left_column

    @property
    @abstractmethod
    def shape(self):
        pass

    @property
    @abstractmethod
    def collision_columns(self):
        pass

    @abstractmethod
    def place_on_grid(self, grid):
        pass

    def get_visible_rows_in_collision_columns(self, grid: Grid):
        return [grid.get_visible_row_by_column(column) for column in self.collision_columns]

    def finalize_placement(self, grid: Grid, rows_for_placement: List[Row], height: int):
        for row, columns in enumerate(self.shape):
            shifted_columns = (column + self.offset for column in columns)
            grid.fill_columns_in_row(rows_for_placement[row], shifted_columns, height+row)

class IJLQBlock(Tetrimino):

    def place_on_grid(self, grid: Grid):
        """
        Place I, J, L or Q block on grid. These four blocks will be placed depending on the row
        the bottom row of block pieces collide with.
        """
        visible_rows = self.get_visible_rows_in_collision_columns(grid)

        # the I, J, L or Q block is placed on top of the highest visible row
        highest_visible_row = max(visible_rows)
        rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))
        starting_height_for_block = highest_visible_row.height + 1

        # finalize block placement on grid
        self.finalize_placement(grid, rows_for_placement, starting_height_for_block)

class IBlock(IJLQBlock):

    shape = [[0, 1, 2, 3]]
    collision_columns = [[0, 1, 2, 3]]

class LBlock(IJLQBlock):

    shape = [[0, 1], [0], [0]]
    collision_columns = [0, 1]

class JBlock(IJLQBlock):

    shape = [[0, 1], [1], [1]]
    collision_columns = [0, 1]

class QBlock(IJLQBlock):

    shape = [[0, 1], [0, 1]]
    collision_columns = [0, 1]

class TBlock(Tetrimino):
    
    shape = [[1], [0, 1, 2]]
    collision_columns = [0, 1, 2]

    def place_on_grid(self, grid: Grid):
        """
        Place T block on grid.
        In cases 1-3, the starting height for the block is the same height as the visible
        row where the collision occurs. In case 4, the starting height for the block is one
        row higher than the visible row where the collision occurs.
        """
        visible_rows = self.get_visible_rows_in_collision_columns(grid)
        
        # Case 1: T block hangs on left side
        if visible_rows[0] > visible_rows[1] and visible_rows[0] > visible_rows[2]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[0], len(self.shape), True)
            starting_height_for_block = visible_rows[0].height
        # Case 2: T block hangs on right side
        elif visible_rows[2] > visible_rows[1] and visible_rows[2] > visible_rows[0]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[2], len(self.shape), True)
            starting_height_for_block = visible_rows[2].height
        # Case 3: T block hangs on both left and right sides
        elif visible_rows[0] > visible_rows[1] and visible_rows[0] == visible_rows[2]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[0], len(self.shape), True)
            starting_height_for_block = visible_rows[0].height
        # Case 4: the bottom of the T is immediately on top of another block.
        else:
            rows_for_placement = grid.get_next_n_rows(visible_rows[1], len(self.shape))
            starting_height_for_block = visible_rows[1].height + 1

        # finalize block placement on grid
        self.finalize_placement(grid, rows_for_placement, starting_height_for_block)

class SBlock(Tetrimino):

    shape = [[0, 1], [1, 2]]
    collision_columns = [0, 1, 2]

    def place_on_grid(self, grid: Grid):
        """
        Place S block on grid.
        In case 1, the starting height for the block is the same height as the visible
        row where the collision occurs. In case 2, the starting height for the block is one
        row higher than the visible row where the collision occurs.
        """
        visible_rows = self.get_visible_rows_in_collision_columns(grid)
        
        # Case 1: S block hangs on the right side or fits "perfectly"
        if visible_rows[2] > visible_rows[0] and visible_rows[2] > visible_rows[1]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[2], len(self.shape), True)
            starting_height_for_block = visible_rows[2].height
        # Case 2: the bottom row of the S block is immediately on top of another block
        else:
            highest_visible_row = visible_rows[0] if visible_rows[0] > visible_rows[1] else visible_rows[1]
            rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))
            starting_height_for_block = highest_visible_row.height + 1

        # finalize block placement on grid
        self.finalize_placement(grid, rows_for_placement, starting_height_for_block)


class ZBlock(Tetrimino):

    shape = [[1, 2], [0, 1]]
    collision_columns = [0, 1, 2]

    def place_on_grid(self, grid: Grid):
        """
        Place Z block on grid.
        In case 1, the starting height for the block is the same height as the visible
        row where the collision occurs. In case 2, the starting height for the block is one
        row higher than the visible row where the collision occurs.
        """
        visible_rows = self.get_visible_rows_in_collision_columns(grid)
        
        # Case 1: Z block hangs on the left side or fits "perfectly"
        if visible_rows[0] > visible_rows[1] and visible_rows[0] > visible_rows[2]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[0], len(self.shape), True)
            starting_height_for_block = visible_rows[0].height
        # Case 2: the bottom row of the S block is immediately on top of another block
        else:
            highest_visible_row = visible_rows[2] if visible_rows[2] > visible_rows[1] else visible_rows[1]
            rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))
            starting_height_for_block = highest_visible_row.height + 1

        # finalize block placement on grid
        self.finalize_placement(grid, rows_for_placement, starting_height_for_block)