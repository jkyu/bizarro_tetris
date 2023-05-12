from abc import ABC, abstractmethod
from typing import List

from simpletetris.grid import Grid, Row, VisibleRow


class Tetrimino(ABC):
    """
    Base class for tetris blocks.

    Attributes
    ----------
    offset: int
        This is the offset from the left column for a given block.
        For example, an offset == 1 means the leftmost column occupied
        by the block is column 1. This is used to shift the block
        into the correct horizontal placement.
    shape: List[List[int]]
        A coordinate representation of the block as if its leftmost
        column were 0. Each inner list represents a row and contains
        the columns occupied by the shape.
    collision_columns: List[int]
        List of column indices indicating the columns that need to be
        checked in order to place a block. A new tetris block will come
        to rest at its collision point. The column indices are as if
        the left column of the block is 0.
    """

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
        """
        Collect information necessary to place the tetris block in the grid
        and then place it in the grid.

        Parameters
        ----------
        grid: Grid
            The tetris grid in its current state.
        """
        visible_rows = self.get_visible_rows_in_collision_columns(grid)
        rows_for_placement = self.get_rows_for_placement(grid, visible_rows)
        self.finalize_placement(grid, rows_for_placement)

    def get_visible_rows_in_collision_columns(self, grid: Grid) -> List[VisibleRow]:
        """
        Find the highest row in each column where the tetris block has the
        potential for collision. The block's offset is used to correctly
        determine the horizontal positioning of the block.

        Parameters
        ----------
        grid: Grid
            The tetris grid in its current state.
        """
        return [grid.get_visible_row_by_column(column+self.offset) for column in self.collision_columns]

    def finalize_placement(self, grid: Grid, rows_for_placement: List[Row]):
        """
        Shift the block by its horizontal offset and then place it into
        the rows of the grid where it belongs.

        Parameters
        ----------
        grid: Grid
            The tetris grid in its current state.
        rows_for_placement: List[Row]
            The list of rows that the tetris block will occupy after
            placement into the grid.
        """
        for row, columns in enumerate(self.shape):
            shifted_columns = [column + self.offset for column in columns]
            grid.fill_columns_in_row(rows_for_placement[row], shifted_columns)

    @abstractmethod
    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        pass

class BottomRowCollisionOnlyBlock(Tetrimino):
    """
    A subset of tetris blocks only has collision points on the bottom row
    of the block. For standard tetris, these are the I, J, L, Q blocks.
    This class serves as a base class for that subset.
    """

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """
        Return the rows in which the block should be placed. The new block
        will be placed on top of the highest visible row in the same columns
        as the block.
        
        Parameters
        ----------
        grid: Grid
            The tetris grid in its current state.
        visible_rows: List[VisibleRows]
            The visible rows that are in the same column as this block.
            The collision will occur with whichever visible row is currently
            highest in the stack in these columns.
        """
        highest_visible_row = max(visible_rows)
        rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))
        return rows_for_placement

class IBlock(BottomRowCollisionOnlyBlock):
    """A class that models the I-block"""

    shape = [[0, 1, 2, 3]]
    collision_columns = [0, 1, 2, 3]

class LBlock(BottomRowCollisionOnlyBlock):
    """A class that models the L-block"""

    shape = [[0, 1], [0], [0]]
    collision_columns = [0, 1]

class JBlock(BottomRowCollisionOnlyBlock):
    """A class that models the J-block"""

    shape = [[0, 1], [1], [1]]
    collision_columns = [0, 1]

class QBlock(BottomRowCollisionOnlyBlock):
    """A class that models the Q-block"""

    shape = [[0, 1], [0, 1]]
    collision_columns = [0, 1]

class TBlock(Tetrimino):
    """A class that models the T-block"""
    
    shape = [[1], [0, 1, 2]]
    collision_columns = [0, 1, 2]

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """
        Return the rows in which the T-block should be placed. There are four
        cases that determine the placement of the T-block. In cases 1-3, the
        starting height for the block is the same height as the visible row
        where the collision occurs. In case 4, the starting height for the block
        is one row higher than the visible row where the collision occurs.

        Parameters
        ----------
        grid: Grid
            The tetris grid in its current state.
        visible_rows: List[VisibleRows]
            The visible rows that are in the same column as this block.
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
    """A class that models the S-block"""

    shape = [[0, 1], [1, 2]]
    collision_columns = [0, 1, 2]

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """
        Return the rows in which the S-block should be placed. There are two
        cases that determine placement of the S-block. In case 1, the starting
        height for the block is the same height as the visible row where the
        collision occurs. In case 2, the starting height for the block is one
        row higher than the visible row where the collision occurs.

        Parameters
        ----------
        grid: Grid
            The tetris grid in its current state.
        visible_rows: List[VisibleRows]
            The visible rows that are in the same column as this block.
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
    """A class that models the Z-block"""

    shape = [[1, 2], [0, 1]]
    collision_columns = [0, 1, 2]

    def get_rows_for_placement(self, grid: Grid, visible_rows: List[VisibleRow]) -> List[Row]:
        """
        Return the rows in which the Z-block should be placed. There are two
        cases that determine placement of the S-block. In case 1, the starting
        height for the block is the same height as the visible row where the
        collision occurs. In case 2, the starting height for the block is one
        row higher than the visible row where the collision occurs.

        Parameters
        ----------
        grid: Grid
            The tetris grid in its current state.
        visible_rows: List[VisibleRows]
            The visible rows that are in the same column as this block.
        """
        # Case 1: Z block hangs on the left side or fits "perfectly"
        if visible_rows[0] > visible_rows[1] and visible_rows[0] > visible_rows[2]:
            rows_for_placement = grid.get_next_n_rows(visible_rows[0], len(self.shape), True)
        # Case 2: the bottom row of the S block is immediately on top of another block
        else:
            highest_visible_row = visible_rows[2] if visible_rows[2] > visible_rows[1] else visible_rows[1]
            rows_for_placement = grid.get_next_n_rows(highest_visible_row, len(self.shape))

        return rows_for_placement