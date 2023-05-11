class Row:
    def __init__(self, prev_row=None, next_row=None):
        self.prev_row = prev_row
        self.next_row = next_row
        self.empty_columns = set(range(10))

    def is_complete(self):
        return len(self.empty_columns) == 0

    def place_in_column(self, column: int):
        self.empty_columns.remove(column)

class Floor:
    """Head sentinel node."""
    def __init__(self):
        self.next_row = None

class Ceiling:
    """Tail sentinel node."""
    def __init__(self):
        self.prev_row = None