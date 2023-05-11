from simpletetris.row import Row, Floor, Ceiling
from typing import List, Tuple

NUM_COLUMNS = 10
MAX_TIMESTAMP = 1000

class VisibleRow:
    """Tracker for the row that is visible from the top of the stack."""
    def __init__(self, row: Row, height: int):
        self.row = row

    @property
    def timestamp(self):
        return self.row.timestamp

    def __gt__(self, other):
        return self.timestamp > other.timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp

class Grid:
    def __init__(self):
        # set up sentinels
        self.floor = Floor()
        self.ceiling = Ceiling()
        self.floor.next_row = self.ceiling
        self.ceiling.prev_row = self.floor

        # set up tracker for stack height
        self.height = 0
        self.timestamp = 0

        # set up hash map to track the highest row in each column
        # these rows are 'visible' from the top of the stack
        self.visible_rows = [VisibleRow(self.floor, 0) for _ in range(NUM_COLUMNS)]

    def print_grid(self):
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
        return self.visible_rows[column]

    def get_next_n_rows(self, visible_row: VisibleRow, n: int, include_current_row: bool = False) -> List[Row]:
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
        Re-stamp all rows if the max timestamp is exceeded.
        This works because rows are timestamped in monotonic order.
        """
        if self.timestamp > MAX_TIMESTAMP:
            new_stamp = 0
            curr_row = self.floor.next_row
            while curr_row is not self.ceiling:
                new_stamp += 1
                curr_row.timestamp = new_stamp

    def get_next_row_or_make_new_row(self, curr_row: Row) -> Row:
        # if next row is the tail sentinel, make a new row and insert it
        if curr_row.next_row is self.ceiling:
            self.timestamp += 1
            self.prevent_timestamp_overflow()
            new_row = Row(
                prev_row = curr_row,
                next_row = self.ceiling,
                timestamp=self.timestamp,
                num_columns=NUM_COLUMNS
            )
            curr_row.next_row = new_row
            self.ceiling.prev_row = new_row
            # increment stack height every time a new row is made
            self.height += 1
        return curr_row.next_row

    def fill_columns_in_row(self, row: Row, columns: List[int]):
        # print("visible before placement: ", [x.row.timestamp for x in self.visible_rows])
        for column in columns:
            row.place_in_column(column)
        # clear the row if it is complete or update row visibility
        if row.is_complete():
            self.remove_row(row)
        else:
            # update row visiblity in the column
            # the only time row visibility does not need to be updated is when
            # the addition(s) to the row immediately clears it, since remove_row()
            # also updates visibility if necessary
            for column in columns:
                if row.timestamp > self.visible_rows[column].timestamp:
                    self.visible_rows[column].row = row
        # print("visible after placement: ", [x.row.timestamp for x in self.visible_rows])
    
    def remove_row(self, row: Row):
        """Remove row from the doubly linked list and update visible rows if necessary"""
        row.prev_row.next_row = row.next_row
        row.next_row.prev_row = row.prev_row
        # decrement stack height when a row is removed
        self.height -= 1

        # the visible rows need to be updated if the row removed was a visible row
        # at worst, we perform roughly equivalent work to shifting the whole grid
        # the expectation is 
        for col in range(len(self.visible_rows)):
            # if the removed row was visible, it needs to be updated
            if row is self.visible_rows[col].row:
                curr_row = row.prev_row
                # seek until the new visible row is found (first row where the column is not empty)
                # or the floor is reached
                while curr_row is not self.floor and col in curr_row.empty_columns:
                    curr_row = curr_row.prev_row
                self.visible_rows[col].row = curr_row