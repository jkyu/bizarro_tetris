import pytest

from simpletetris.grid import Grid, Row, VisibleRow


@pytest.fixture
def grid():
    grid = Grid()
    grid.timestamp = 2
    grid.height = 2

    # place two rows in the grid
    row1 = Row(prev_row=grid.floor, next_row=None, timestamp=1)
    row2 = Row(prev_row=row1, next_row=grid.ceiling, timestamp=2)
    row1.next_row = row2
    grid.floor.next_row = row1
    grid.ceiling.prev_row = row2

    # the test grid looks like this:
    # ooooooooo-
    # --------oo
    row1.empty_columns = set(range(8))
    row2.empty_columns = {9}

    grid.visible_rows = [VisibleRow(row2) for _ in range(9)] + [VisibleRow(row1)]
    return grid


def get_num_rows(grid: Grid) -> int:
    """
    Count the number of rows explicitly by traversing the doubly linked
    list of rows in the grid.
    """
    # count the rows explicitly
    n_rows = 0
    curr_row = grid.floor.next_row
    while curr_row is not grid.ceiling:
        n_rows += 1
        curr_row = curr_row.next_row
    return n_rows


class TestGrid:
    def test_prevent_timestamp_overflow(self, grid: Grid):
        # make a grid that is currently on timestamp 1001
        grid.timestamp = 1001

        # set the rows in the grid to large timestamps
        row1 = grid.floor.next_row
        row2 = row1.next_row
        row1.timestamp = 999
        row2.timestamp = 1000
        assert row1.timestamp == 999
        assert row2.timestamp == 1000

        # grid and rows should have their timestamps reset
        grid.prevent_timestamp_overflow()
        assert grid.timestamp == 2
        assert row1.timestamp == 1
        assert row2.timestamp == 2

    def test_get_next_row_or_make_new_row_get_next_row(self, grid: Grid):
        """
        Test scenario where get_next_row_or_make_new_row() returns an existing row.
        The height of the grid is incremented when a new row is inserted, so also
        test that the height does not change when returning an existing row.
        """
        curr_row = grid.floor
        expected_row = curr_row.next_row
        expected_height = grid.height
        next_row = grid.get_next_row_or_make_new_row(curr_row)
        assert next_row is expected_row
        # height of grid does not change
        assert grid.height == expected_height

    def test_get_next_row_or_make_new_row_make_new_row(self, grid: Grid):
        """
        Test scenario where get_next_row_or_make_new_row() returns a new row.
        The height of the grid is incremented when a new row is inserted, so also
        test that the height increases when returning an existing row.
        """
        curr_row = grid.ceiling.prev_row
        curr_timestamp = grid.timestamp
        expected_height = grid.height + 1
        next_row = grid.get_next_row_or_make_new_row(curr_row)

        # make sure the ceiling is not returned
        assert next_row is not grid.ceiling
        # new row generated should cause timestamp to increment
        assert grid.timestamp == curr_timestamp + 1
        assert next_row.timestamp == grid.timestamp
        # height of grid increases
        assert grid.height == expected_height

    def test_get_next_n_rows_exclude_current_row_get_existing_rows(self, grid: Grid):
        """
        Test scenario where get_next_n_rows() does not include the current row
        and returns the next n existing rows.
        """
        n_rows = 2
        existing_rows = [grid.floor.next_row, grid.ceiling.prev_row]
        visible_row = VisibleRow(grid.floor)
        next_rows = grid.get_next_n_rows(visible_row, n_rows, False)
        assert len(next_rows) == n_rows
        for expected, actual in zip(existing_rows, next_rows):
            assert actual is expected

    def test_get_next_n_rows_exclude_current_row_make_new_row(self, grid: Grid):
        """
        Test scenario where get_next_n_rows() does not include the current row
        and adds additional rows in order to return the next n rows.
        """
        n_rows = 4
        existing_rows = [grid.floor.next_row, grid.ceiling.prev_row]
        visible_row = VisibleRow(grid.floor)
        next_rows = grid.get_next_n_rows(visible_row, n_rows, False)
        assert len(next_rows) == n_rows

        # ensure existing rows are returned
        assert next_rows[0] is existing_rows[0]
        assert next_rows[1] is existing_rows[1]

        # check that timestamp is incremented appropriately to reflect two added rows
        assert grid.timestamp == 4
        assert next_rows[2].timestamp == 3
        assert next_rows[3].timestamp == 4

    def test_get_next_n_rows_include_current_row_get_existing_rows(self, grid: Grid):
        """
        Test scenario where get_next_n_rows() includes the current row
        and returns the next n existing rows.
        """
        n_rows = 2
        curr_row = grid.floor.next_row
        existing_rows = [curr_row, curr_row.next_row]
        visible_row = VisibleRow(curr_row)
        next_rows = grid.get_next_n_rows(visible_row, n_rows, True)
        assert len(next_rows) == n_rows
        for expected, actual in zip(existing_rows, next_rows):
            assert actual is expected

    def test_get_next_n_rows_include_current_row_make_new_row(self, grid: Grid):
        """
        Test scenario where get_next_n_rows() includes the current row
        and adds additional rows in order to return the next n rows.
        """
        n_rows = 4
        curr_row = grid.floor.next_row
        existing_rows = [curr_row, curr_row.next_row]
        visible_row = VisibleRow(curr_row)
        next_rows = grid.get_next_n_rows(visible_row, n_rows, True)
        assert len(next_rows) == n_rows

        # ensure existing rows are returned
        assert next_rows[0] is existing_rows[0]
        assert next_rows[1] is existing_rows[1]

        # check that timestamp is incremented appropriately to reflect two added rows
        assert grid.timestamp == 4
        assert next_rows[2].timestamp == 3
        assert next_rows[3].timestamp == 4

    def test_remove_row_no_visibility_update(self, grid: Grid):
        """
        Test removal of a row that will not change the visibility.
        To do this, we will add a new third row so that the grid looks like
            3|xxxxxxxxx-|
            2|ooooooooo-|
            1|--------ox|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        We will drop a special one cell block to remove the second row.
        Row visibility should not change. The final grid should be
            3|xxxxxxxxx-|
            1|--------ox|
        """
        row2 = grid.ceiling.prev_row
        row3 = Row(prev_row=row2, next_row=grid.ceiling, timestamp=3)
        row2.next_row = row3
        grid.ceiling.prev_row = row3
        grid.height += 1
        assert grid.height == 3
        for i in range(9):
            grid.visible_rows[i].row = row3
            assert grid.visible_rows[i].timestamp == row3.timestamp
        expected_visible_row_timestamps = [3] * 9 + [1]
        expected_height = grid.height - 1

        grid.remove_row(row2)
        # height drops by 1
        assert grid.height == expected_height
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_remove_row_with_visibility_update(self, grid: Grid):
        """
        Test removal of a row that changes the visibility.
        The test grid looks like the following:
            2|xxxxxxxxx-|
            1|--------ox|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        Removing row 1 will cause visibility to change in the rightmost column,
        where the new visible row will be the floor.
        """
        row1 = grid.floor.next_row
        expected_visible_row_timestamps = [2] * 9 + [0]
        expected_height = grid.height - 1

        grid.remove_row(row1)
        # height drops by 1
        assert grid.height == expected_height
        # visibility should be updated to match the expected
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_fill_columns_in_row_remove_row(self, grid: Grid):
        """
        Test addition to row 2 that will remove it.
        The test grid looks like the following:
            2|xxxxxxxxx-|
            1|--------ox|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        Column 9 will be added to row 2, which will complete it and trigger
        row removal.
        """
        row2 = grid.ceiling.prev_row
        expected_height = grid.height - 1
        expected_visible_row_timestamps = [0] * 8 + [1] * 2

        grid.fill_columns_in_row(row2, [9])
        # check height is reduced by 1 due to row removal
        assert grid.height == expected_height
        assert get_num_rows(grid) == expected_height
        # ensure visibility does not change
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_fill_columns_in_row_update_visible_rows(self, grid: Grid):
        """
        Test addition to row 2 that will remove it.
        Row 2 will be changed to have a few extra holes to fill.
        The test grid looks like the following:
            2|--xxxxxxx-|
            1|--------ox|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        Columns 0 and 1 will be added to row 2, which will complete it and trigger
        row removal.
        """
        # remove cols 0 and 1 from row 2 to set up the test
        row2 = grid.ceiling.prev_row
        row2.empty_columns.add(0)
        row2.empty_columns.add(1)
        grid.visible_rows[0].row = grid.floor
        grid.visible_rows[1].row = grid.floor
        expected_height = grid.height
        expected_visible_row_timestamps = [2] * 9 + [1]
        current_visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert expected_visible_row_timestamps != current_visible_row_timestamps

        grid.fill_columns_in_row(row2, [0, 1])
        # check height does not change
        assert grid.height == expected_height
        assert get_num_rows(grid) == expected_height
        # verify that visibility changed
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps
