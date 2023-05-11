from abc import ABC, abstractmethod

class Tetrimino(ABC):

    def __init__(self, left_column):
        self.left_column = left_column
        self.columns_to_check = self.get_columns_to_check(left_column)

    @abstractmethod
    def get_columns_to_check(self, left_column):
        pass

    @abstractmethod
    def place_on_grid(self, grid):
        pass

    @abstractmethod
    def get_rows_for_placement(self, grid):
        pass

class Q_block(Tetrimino):

    def get_columns_to_check(self, left_column):
        return (left_column, left_column+1)

    def place_on_grid(self, grid):
        """
        Resolve collisions and return the lowest row the block will occupy.
        Place Q block on grid. If the rows currently do not exist, they will be generated.
        """
        left_col, right_col = self.columns_to_check
        left_row = grid.get_curr_row_by_column(left_col)
        right_row = grid.get_curr_row_by_column(right_col)
        curr_row = max(left_row, right_row)
        rows_for_placement = grid.get_next_n_rows(curr_row, 2)
        for i, row in enumerate(rows_for_placement):
            grid.fill_columns_in_row(row, self.columns_to_check, curr_row.height+i+1)

class Z_block(Tetrimino):
    
    def get_columns_to_check(self, left_column):
        return (left_column, left_column+1, left_column+2)

    def get_rows_for_placement(self, grid):
        curr_highest_rows = [grid.get_curr_row_by_column(col) for col in self.columns_to_check]
        # check for cliffhanger pattern - this works with the edge condition where
        # all three columns are of equal height, e.g., in the case of a clean grid
        if curr_highest_rows[0] > curr_highest_rows[1] and curr_highest_rows[0] > curr_highest_rows[2]:
            curr_row = grid.get_curr_row_by_column(self.columns_to_check[0])
            rows_for_placement = grid.get_next_n_rows(curr_row.prev_row)
        # not cliffhanger, so place on top of whichever of cols 1 or 2 is higher
        else:
            curr_row = max(
                grid.get_curr_row_by_column(self.columns_to_check[1]),
                grid.get_curr_row_by_column(self.columns_to_check[2])
            )
            rows_for_placement = grid.get_next_n_rows(curr_row)
        return rows_for_placement