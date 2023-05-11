class Row:
    def __init__(self, prev_row=None, next_row=None, timestamp=0, num_columns=10):
        self.prev_row = prev_row
        self.next_row = next_row
        self.empty_columns = set(range(num_columns))
        self.timestamp = timestamp

    def is_complete(self):
        return len(self.empty_columns) == 0

    def place_in_column(self, column: int):
        self.empty_columns.remove(column)

class Floor:
    """Head sentinel node."""
    def __init__(self):
        self.next_row = None
        self.timestamp = -1

class Ceiling:
    """Tail sentinel node."""
    def __init__(self):
        self.prev_row = None
        self.timestamp = float("inf")