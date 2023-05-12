from typing import List

NUM_COLUMNS = 10
MAX_TIMESTAMP = 1000

class Row:
    """
    A class for modeling each row in the tetris grid. It holds information
    about the unoccupied columns under the assumption that the tetris grid
    is usually dense. This serves as a node in the doubly linked list used
    to represent the grid.

    Attributes
    ----------
    prev_row: Row
        This points to the row directly below this row in the current state
        of the grid.
    next_row: Row
        This points to the row directly above this row in the current state
        of the grid.
    empty_columns: Set[int]
        A hash set containing the indices for columns that are currently not
        occupied in this row. A completed row will have an empty set.
    timestamp: int
        A unique identifier for the row. A row with a larger timestamp will
        always be higher in the tetris stack than a row with a smaller timestamp
        because new rows are added to the top of the grid monotonically.
    """
    def __init__(self, prev_row: "Row"=None, next_row: "Row"=None, timestamp: int=0):
        self.prev_row = prev_row
        self.next_row = next_row
        self.empty_columns = set(range(NUM_COLUMNS))
        self.timestamp = timestamp

    def is_complete(self) -> bool:
        return len(self.empty_columns) == 0

    def place_in_column(self, column: int):
        self.empty_columns.remove(column)

class Floor:
    """
    A sentinel node that serves as the bottom of the grid.
    The floor cannot be occupied by a tetris block.

    Attributes
    ----------
    next_row: Row
        The row directly above the bottom of the grid. It is either the
        first row of the tetris stack or the ceiling when the grid is empty
    timestamp: int
        The minimum timestamp. All other rows have larger timestamps.
    """
    def __init__(self):
        self.next_row = None
        self.timestamp = 0

class Ceiling:
    """
    A sentinel node that serves as the top of the grid.
    The ceiling cannot be occupied by a tetris block.

    Attributes
    ----------
    prev_row: Row
        The row directly below the top of the grid. It is either the
        highest row of the tetris stack or the floor when the grid is empty
    timestamp: int
        The maximum timestamp. All other rows have smaller timestamps.
    """
    def __init__(self):
        self.prev_row = None
        self.timestamp = float("inf")

class VisibleRow:
    """
    A class that tracks the row visible from the top of each column.
    In other words, the visible row is the highest row in a column.
    Only visible rows are candidates for collisions with newly introduced
    tetris pieces.

    Attributes
    ----------
    row: Row
        the row that is currently visible
    """
    def __init__(self, row: Row):
        self.row = row

    @property
    def timestamp(self):
        return self.row.timestamp

    def __gt__(self, other: "VisibleRow") -> bool:
        return self.timestamp > other.timestamp

    def __eq__(self, other: "VisibleRow") -> bool:
        return self.timestamp == other.timestamp

class Grid:
    """
    A class that represents the tetris grid and all operations on the grid.
    The grid is represented as a doubly linked list of rows.

    Attributes:
    ----------
    floor: Row
        A marker for the bottom of the grid. This serves as the head sentinel for
        the linked list and does not count toward the height of the tetris stack.
    ceiling: Row
        A marker for the top of the grid. This serves as the tail sentinel for the
        linked list and does not count toward the height of the tetris stack.
    height: int
        The height of the stack. This is the maximum height over all of the columns
        at any time.
    timestamp: int
        A counter for the unique number of rows that have been occupied in the grid.
        Because the grid is represented as a linked list, a cleared line simply
        disappears from the grid. New rows are introduced to the tetris stack
        monotonically, so the timestamp is a unique and ordered identifier for each row.
    visible_rows: List[VisibleRow]
        An index for the currently visible row in each column.
    """
    def __init__(self):
        # set up doubly-linked list of rows with floor and ceiling sentinels.
        self.floor = Floor()
        self.ceiling = Ceiling()
        self.floor.next_row = self.ceiling
        self.ceiling.prev_row = self.floor

        self.height = 0
        self.timestamp = 0

        # the only row that is initially visible is the floor
        self.visible_rows = [VisibleRow(self.floor) for _ in range(NUM_COLUMNS)]

    def print_grid(self):
        """
        Print the tetris board out to command line. "o" indicates an occupied
        cell in the grid and "-" indicates an empty cell.
        """
        print(f"Grid State: stack height = {self.height}")
        curr_row = self.ceiling.prev_row
        while curr_row is not self.floor:
            line = ["o"]*NUM_COLUMNS
            for empty_column in curr_row.empty_columns:
                line[empty_column] = "-"
            print(f"{curr_row.timestamp:<3}|" + "".join(line) + "|")
            curr_row = curr_row.prev_row
        print("   |0123456789|")

    def get_visible_row_by_column(self, column: int) -> VisibleRow:
        """
        Return the currently visible row in a specified column.

        Parameters
        ----------
        column: int
        """
        return self.visible_rows[column]

    def get_next_n_rows(self, visible_row: VisibleRow, n: int, include_current_row: bool = False) -> List[Row]:
        """
        Return the next n rows starting from the visible_row. If not enough
        rows currently exist in the grid, they will be created so that n rows
        can be returned.

        Parameters
        ----------
        visible_row: VisibleRow
            The row from which to start counting.
        n: int
            Number of rows to retrieve.
        include_current_row: bool
            Whether to include the currently visible row in the n rows returned.
        """
        next_n_rows = []
        curr_row = visible_row.row
        if include_current_row:
            next_n_rows.append(curr_row)
            n -= 1
        for _ in range(n):
            curr_row = self.get_next_row_or_make_new_row(curr_row)
            next_n_rows.append(curr_row)
        return next_n_rows

    def prevent_timestamp_overflow(self):
        """
        Re-stamp all rows if the max timestamp is exceeded. This works because rows
        are timestamped in monotonic order. This also assumes that the grid will
        never have more than MAX_TIMESTAMP simultaneous rows.
        """
        if self.timestamp > MAX_TIMESTAMP:
            new_stamp = 0
            curr_row = self.floor.next_row
            while curr_row is not self.ceiling:
                new_stamp += 1
                curr_row.timestamp = new_stamp
                curr_row = curr_row.next_row
            self.timestamp = new_stamp

    def get_next_row_or_make_new_row(self, curr_row: Row) -> Row:
        """
        If next row is the tail sentinel, make a new row and insert it.

        Parameters
        ----------
        curr_row: Row
        """
        if curr_row.next_row is self.ceiling:
            self.timestamp += 1
            self.prevent_timestamp_overflow()
            new_row = Row(
                prev_row = curr_row,
                next_row = self.ceiling,
                timestamp=self.timestamp
            )
            curr_row.next_row = new_row
            self.ceiling.prev_row = new_row
            # increment stack height every time a new row is made
            self.height += 1
        return curr_row.next_row

    def fill_columns_in_row(self, row: Row, columns: List[int]):
        """
        Fills columns in a row. Every move is assumed valid, so there
        is no protection against illegal moves here. If a row is completed
        by filling the specified columns, the row will be removed. Otherwise,
        row visibility will be updated as necessary.

        Parameters
        ----------
        row: Row
        columns: List[int]
            The columns that will be occupied in this row.
        """
        for column in columns:
            row.place_in_column(column)
        # clear the row if it is complete or update row visibility
        if row.is_complete():
            self.remove_row(row)
        else:
            for column in columns:
                if row.timestamp > self.visible_rows[column].timestamp:
                    self.visible_rows[column].row = row
    
    def remove_row(self, row: Row):
        """
        Remove row from the doubly linked list and update visible rows if necessary.
        The visible rows need to be updated if the row removed was visible in any column.
        The expectation for normal tetris is that this would save signficant work, since
        cleared rows are not necessarily near the top of the stack. In this simplified
        tetris, rows generally will be removed closer to the top of the stack, but this
        still saves work in that work to find the newly visible row only needs to be performed
        upon removing a currently visible row.

        Parameters
        ----------
        row: Row
        """
        row.prev_row.next_row = row.next_row
        row.next_row.prev_row = row.prev_row
        # decrement stack height when a row is removed
        self.height -= 1

        # update row visibility
        for col in range(len(self.visible_rows)):
            # if the removed row was visible, it needs to be updated
            if row is self.visible_rows[col].row:
                curr_row = row.prev_row
                # seek until the new visible row is found (first row where the column is not empty)
                # or the floor is reached
                while curr_row is not self.floor and col in curr_row.empty_columns:
                    curr_row = curr_row.prev_row
                self.visible_rows[col].row = curr_row