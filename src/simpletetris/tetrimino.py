from simpletetris.grid import Grid, VisibleRow
from simpletetris.row import Row
from abc import ABC, abstractmethod
from typing import List

class Tetrimino(ABC):

    def __init__(self, offset):
        self.offset = offset

    @property
    @abstractmethod
    def shape(self):
        pass

    @property
    @abstractmethod
    def collision_columns(self):
        pass

    def place_on_grid(self, grid: Grid):
        visible_rows = self.get_visible_rows_in_collision_columns(grid)
        rows_for_placement = self.get_rows_for_placement(grid, visible_rows)
        self.finalize_placement(grid, rows_for_placement)

    def get_visible_rows_in_collision_columns(self, grid: Grid) -> List[VisibleRow]:
        return [grid.get_visible_row_by_column(column+self.offset) for column in self.collision_columns]

    def finalize_placement(self, grid: Grid, rows_for_placement: List[Row]):
        for row, columns in enumerate(self.shape):
            shifted_columns = [column + self.offset for column in columns]
            grid.fill_columns_in_row(rows_for_placement[row], shifted_columns)

    @abstractmethod
    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        pass

class BottomRowCollisionOnlyBlock(Tetrimino):

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """Place block on top of the highest visible row."""
        highest_visible_row = max(visible_rows)
        rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))
        return rows_for_placement

class IBlock(BottomRowCollisionOnlyBlock):

    shape = [[0, 1, 2, 3]]
    collision_columns = [0, 1, 2, 3]

class LBlock(BottomRowCollisionOnlyBlock):

    shape = [[0, 1], [0], [0]]
    collision_columns = [0, 1]

class JBlock(BottomRowCollisionOnlyBlock):

    shape = [[0, 1], [1], [1]]
    collision_columns = [0, 1]

class QBlock(BottomRowCollisionOnlyBlock):

    shape = [[0, 1], [0, 1]]
    collision_columns = [0, 1]

class TBlock(Tetrimino):
    
    shape = [[1], [0, 1, 2]]
    collision_columns = [0, 1, 2]

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """
        In cases 1-3, the starting height for the block is the same height as the visible
        row where the collision occurs. In case 4, the starting height for the block is one
        row higher than the visible row where the collision occurs.
        """
        # Case 1: T block hangs on left side
        if visible_rows[0] > visible_rows[1] and visible_rows[0] > visible_rows[2]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[0], len(self.shape), True)
        # Case 2: T block hangs on right side
        elif visible_rows[2] > visible_rows[1] and visible_rows[2] > visible_rows[0]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[2], len(self.shape), True)
        # Case 3: T block hangs on both left and right sides
        elif visible_rows[0] > visible_rows[1] and visible_rows[0] == visible_rows[2]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[0], len(self.shape), True)
        # Case 4: the bottom of the T is immediately on top of another block.
        else:
            rows_for_placement = grid.get_next_n_rows(visible_rows[1], len(self.shape))

        return rows_for_placement

class SBlock(Tetrimino):

    shape = [[0, 1], [1, 2]]
    collision_columns = [0, 1, 2]

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """
        In case 1, the starting height for the block is the same height as the visible
        row where the collision occurs. In case 2, the starting height for the block is one
        row higher than the visible row where the collision occurs.
        """
        # Case 1: S block hangs on the right side or fits "perfectly"
        if visible_rows[2] > visible_rows[0] and visible_rows[2] > visible_rows[1]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[2], len(self.shape), True)
        # Case 2: the bottom row of the S block is immediately on top of another block
        else:
            highest_visible_row = visible_rows[0] if visible_rows[0] > visible_rows[1] else visible_rows[1]
            rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))

        return rows_for_placement


class ZBlock(Tetrimino):

    shape = [[1, 2], [0, 1]]
    collision_columns = [0, 1, 2]

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """
        In case 1, the starting height for the block is the same height as the visible
        row where the collision occurs. In case 2, the starting height for the block is one
        row higher than the visible row where the collision occurs.
        """
        # Case 1: Z block hangs on the left side or fits "perfectly"
        if visible_rows[0] > visible_rows[1] and visible_rows[0] > visible_rows[2]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[0], len(self.shape), True)
        # Case 2: the bottom row of the S block is immediately on top of another block
        else:
            highest_visible_row = visible_rows[2] if visible_rows[2] > visible_rows[1] else visible_rows[1]
            rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))

        return rows_for_placement