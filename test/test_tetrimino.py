import pytest

from simpletetris import tetris
from simpletetris.grid import Grid
from simpletetris.row import Row


@pytest.fixture
def grid_two_rows():
    grid = Grid()
    grid.timestamp = 2
    grid.height = 2

    # place two rows in the grid
    row1 = Row(prev_row = grid.floor, next_row = None, timestamp = 1)
    row2 = Row(prev_row = row1, next_row = grid.ceiling, timestamp = 2)
    row1.next_row = row2
    grid.floor.next_row = row1
    grid.ceiling.prev_row = row2
    return grid

@pytest.fixture
def grid_one_row():
    """
    Set up grid to look like this:
        1|--xxx---x-|
    where "x" marks a visible cell, "o" marks an occupied but not visible
    cell, "-" marks an empty cell, and the number of the left is the timestamp.
    """
    grid = Grid()
    grid.timestamp = 1
    grid.height = 1

    # place one row in the grid
    row = Row(prev_row = grid.floor, next_row = grid.ceiling, timestamp = 1)
    grid.floor.next_row = row
    grid.ceiling.prev_row = row

    # set up grid for tests
    row = grid.floor.next_row
    row.empty_columns = {0, 1, 5, 6, 7, 9}
    for i in (2, 3, 4, 8):
        grid.visible_rows[i].row = row

    return grid

class TestIBlock:
    def test_iblock_drop(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding I4, it should become:
            2|----xxxx--|
            1|--xxo---x-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 6, 7, 9}
        expected_row2_empty_cols = {0, 1, 2, 3, 8, 9}
        expected_height = grid.height + 1
        expected_visible_row_timestamps = [0]*2 + [1]*2 + [2]*4 + [1, 0]

        block = tetris.spawn_tetrimino("I", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_iblock_clear(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|-------xxx|
            1|x----xxooo|
        After adding I1, it should become:
            2|-------xxx|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1, 2, 3, 4}
        row2.empty_columns = {0, 1, 2, 3, 4, 5, 6}
        for i in (0, 5, 6):
            grid.visible_rows[i].row = row1
        for i in (7, 8, 9):
            grid.visible_rows[i].row = row2

        expected_row_empty_cols = set(row2.empty_columns)
        expected_height = grid.height - 1
        expected_visible_row_timestamps = [0]*7 + [2]*3

        block = tetris.spawn_tetrimino("I", 1)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row = grid.floor.next_row
        assert row.empty_columns == expected_row_empty_cols
        assert row.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

class TestJBlock:
    def test_jblock_drop(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding J4, it should become:
            4|-----x----|
            3|-----o----|
            2|----xo----|
            1|--xxo---x-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 6, 7, 9}
        expected_row2_empty_cols = set(range(10)) - {4, 5}
        expected_row3_empty_cols = set(range(10)) - {5}
        expected_row4_empty_cols = set(range(10)) - {5}
        expected_height = grid.height + 3
        expected_visible_row_timestamps = [0, 0, 1, 1, 2, 4, 0, 0, 1, 0]

        block = tetris.spawn_tetrimino("J", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        row3 = row2.next_row
        row4 = row3.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2
        assert row3.empty_columns == expected_row3_empty_cols
        assert row3.timestamp == 3
        assert row4.empty_columns == expected_row4_empty_cols
        assert row4.timestamp == 4

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_jblock_clear(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|-------xxx|
            1|x--xxxxooo|
        After adding J1, it should become:
            3|--x-------|
            2|--o----xxx|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1, 2}
        row2.empty_columns = {0, 1, 2, 3, 4, 5, 6}
        for i in (0, 3, 4, 5, 6):
            grid.visible_rows[i].row = row1
        for i in (7, 8, 9):
            grid.visible_rows[i].row = row2

        expected_row1_empty_cols = set(range(10)) - {2, 7, 8, 9}
        expected_row2_empty_cols = set(range(10)) - {2}
        expected_height = grid.height
        expected_visible_row_timestamps = [0, 0, 3] +[0]*4 + [2]*3

        block = tetris.spawn_tetrimino("J", 1)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 2
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 3

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

class TestLBlock:
    def test_lblock_drop(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding L4, it should become:
            4|----x-----|
            3|----o-----|
            2|----ox----|
            1|--xxo---x-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 6, 7, 9}
        expected_row2_empty_cols = set(range(10)) - {4, 5}
        expected_row3_empty_cols = set(range(10)) - {4}
        expected_row4_empty_cols = set(range(10)) - {4}
        expected_height = grid.height + 3
        expected_visible_row_timestamps = [0, 0, 1, 1, 4, 2, 0, 0, 1, 0]

        block = tetris.spawn_tetrimino("L", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        row3 = row2.next_row
        row4 = row3.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2
        assert row3.empty_columns == expected_row3_empty_cols
        assert row3.timestamp == 3
        assert row4.empty_columns == expected_row4_empty_cols
        assert row4.timestamp == 4

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_lblock_clear(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|-------xxx|
            1|x--xxxxooo|
        After adding L1, it should become:
            3|-x--------|
            2|-o-----xxx|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1, 2}
        row2.empty_columns = {0, 1, 2, 3, 4, 5, 6}
        for i in (0, 3, 4, 5, 6):
            grid.visible_rows[i].row = row1
        for i in (7, 8, 9):
            grid.visible_rows[i].row = row2

        expected_row1_empty_cols = set(range(10)) - {1, 7, 8, 9}
        expected_row2_empty_cols = set(range(10)) - {1}
        expected_height = grid.height
        expected_visible_row_timestamps = [0, 3] +[0]*5 + [2]*3

        block = tetris.spawn_tetrimino("L", 1)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 2
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 3

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

class TestQBlock:
    def test_qblock_drop(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding Q4, it should become:
            3|----xx----|
            2|----oo----|
            1|--xxo---x-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 6, 7, 9}
        expected_row2_empty_cols = set(range(10)) - {4, 5}
        expected_row3_empty_cols = set(range(10)) - {4, 5}
        expected_height = grid.height + 2
        expected_visible_row_timestamps = [0, 0, 1, 1, 3, 3, 0, 0, 1, 0]

        block = tetris.spawn_tetrimino("Q", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        row3 = row2.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2
        assert row3.empty_columns == expected_row3_empty_cols
        assert row3.timestamp == 3

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_qblock_clear(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|-------xxx|
            1|x--xxxxooo|
        After adding Q1, it should become:
            2|-xx----xxx|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1, 2}
        row2.empty_columns = {0, 1, 2, 3, 4, 5, 6}
        for i in (0, 3, 4, 5, 6):
            grid.visible_rows[i].row = row1
        for i in (7, 8, 9):
            grid.visible_rows[i].row = row2

        expected_row_empty_cols = {0, 3, 4, 5, 6}
        expected_height = grid.height - 1
        expected_visible_row_timestamps = [0, 2, 2] +[0]*4 + [2]*3

        block = tetris.spawn_tetrimino("Q", 1)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row = grid.floor.next_row
        assert row.empty_columns == expected_row_empty_cols
        assert row.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

class TestTBlock:
    def test_tblock_drop_left_fit(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding T4, it should become:
            2|----xxx---|
            1|--xxoo--x-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 6, 7, 9}
        expected_row2_empty_cols = set(range(10)) - {4, 5, 6}
        expected_height = grid.height + 1
        expected_visible_row_timestamps = [0, 0, 1, 1, 2, 2, 2, 0, 1, 0]

        block = tetris.spawn_tetrimino("T", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_tblock_drop_right_fit(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding T6, it should become:
            2|------xxx-|
            1|--xxx--oo-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 6, 9}
        expected_row2_empty_cols = set(range(10)) - {6, 7, 8}
        expected_height = grid.height + 1
        expected_visible_row_timestamps = [0, 0, 1, 1, 1, 0, 2, 2, 2, 0]

        block = tetris.spawn_tetrimino("T", 6)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_tblock_drop_left_and_right_fit(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx-xxx-|
        After adding T4, it should become:
            2|----xxx---|
            1|--xxoooxx-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for tests
        grid = grid_one_row
        row = grid.floor.next_row
        row.empty_columns = {0, 1, 5, 9}
        for i in (2, 3, 4, 6, 7, 8):
            grid.visible_rows[i].row = row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 9}
        expected_row2_empty_cols = set(range(10)) - {4, 5, 6}
        expected_height = grid.height + 1
        expected_visible_row_timestamps = [0, 0, 1, 1, 2, 2, 2, 1, 1, 0]

        block = tetris.spawn_tetrimino("T", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_tblock_clear_one_line(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|---xxxxxxx|
            1|x--ooooooo|
        After adding T0, it should become:
            1|xx-xxxxxxx|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1, 2}
        row2.empty_columns = {0, 1, 2}
        grid.visible_rows[0].row = row1
        for i in range(3, 10):
            grid.visible_rows[i].row = row2

        expected_row_empty_cols = {2}
        expected_height = grid.height - 1
        expected_visible_row_timestamps = [1, 1, 0] + [1]*7

        block = tetris.spawn_tetrimino("T", 0)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row = grid.floor.next_row
        assert row.empty_columns == expected_row_empty_cols
        assert row.timestamp == 1

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_tblock_clear_two_lines(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|---xxxxxxx|
            1|x-xooooooo|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        After adding T0, we should end up with an empty board.
            1|xx-xxxxxxx|
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1}
        row2.empty_columns = {0, 1, 2}
        grid.visible_rows[0].row = row1
        grid.visible_rows[2].row = row1
        for i in range(3, 10):
            grid.visible_rows[i].row = row2

        expected_height = 0
        expected_visible_row_timestamps = [0]*10

        block = tetris.spawn_tetrimino("T", 0)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        assert grid.floor.next_row is grid.ceiling

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

class TestSBlock:
    def test_sblock_drop_left_overhang(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding S4, it should become:
            3|-----xx---|
            2|----xo----|
            1|--xxo---x-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 6, 7, 9}
        expected_row2_empty_cols = set(range(10)) - {4, 5}
        expected_row3_empty_cols = set(range(10)) - {5, 6}
        expected_height = grid.height + 2
        expected_visible_row_timestamps = [0, 0, 1, 1, 2, 3, 3, 0, 1, 0]

        block = tetris.spawn_tetrimino("S", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        row3 = row2.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2
        assert row3.empty_columns == expected_row3_empty_cols
        assert row3.timestamp == 3

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_sblock_drop_right_fit(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding S6, it should become:
            2|-------xx-|
            1|--xxx-xoo-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 9}
        expected_row2_empty_cols = set(range(10)) - {7, 8}
        expected_height = grid.height + 1
        expected_visible_row_timestamps = [0, 0, 1, 1, 1, 0, 1, 2, 2, 0]

        block = tetris.spawn_tetrimino("S", 6)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_sblock_clear(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|-------xxx|
            1|x--xxxxooo|
        After adding S1, it should become:
            2|--xx---xxx|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1, 2}
        row2.empty_columns = {0, 1, 2, 3, 4, 5, 6}
        for i in (0, 3, 4, 5, 6):
            grid.visible_rows[i].row = row1
        for i in (7, 8, 9):
            grid.visible_rows[i].row = row2

        expected_row_empty_cols = {0, 1, 4, 5, 6}
        expected_height = grid.height - 1
        expected_visible_row_timestamps = [0, 0, 2, 2] +[0]*3 + [2]*3

        block = tetris.spawn_tetrimino("S", 1)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row = grid.floor.next_row
        assert row.empty_columns == expected_row_empty_cols
        assert row.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

class TestZBlock:
    def test_zblock_drop_right_overhang(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding Z6, it should become:
            3|------xx--|
            2|-------ox-|
            1|--xxx---o-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 5, 6, 7, 9}
        expected_row2_empty_cols = set(range(10)) - {7, 8}
        expected_row3_empty_cols = set(range(10)) - {6, 7}
        expected_height = grid.height + 2
        expected_visible_row_timestamps = [0, 0, 1, 1, 1, 0, 3, 3, 2, 0]

        block = tetris.spawn_tetrimino("Z", 6)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        row3 = row2.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2
        assert row3.empty_columns == expected_row3_empty_cols
        assert row3.timestamp == 3

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_zblock_drop_left_fit(self, grid_one_row: Grid):
        """
        The test grid initially looks like the following:
            1|--xxx---x-|
        After adding Z4, it should become:
            2|----xx----|
            1|--xxoox-x-|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        grid = grid_one_row

        # write out expected results
        expected_row1_empty_cols = {0, 1, 7, 9}
        expected_row2_empty_cols = set(range(10)) - {4, 5}
        expected_height = grid.height + 1
        expected_visible_row_timestamps = [0, 0, 1, 1, 2, 2, 1, 0, 1, 0]

        block = tetris.spawn_tetrimino("Z", 4)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row1 = grid.floor.next_row
        row2 = row1.next_row
        assert row1.empty_columns == expected_row1_empty_cols
        assert row1.timestamp == 1
        assert row2.empty_columns == expected_row2_empty_cols
        assert row2.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps

    def test_zblock_clear(self, grid_two_rows: Grid):
        """
        The test grid initially looks like the following:
            2|-------xxx|
            1|x--xxxxooo|
        After adding Z0, it should become:
            2|xx-----xxx|
        where "x" marks a visible cell, "o" marks an occupied but not visible
        cell, "-" marks an empty cell, and the number of the left is the timestamp.
        """
        # set up grid for test
        grid = grid_two_rows
        row1 = grid.floor.next_row
        row2 = grid.ceiling.prev_row
        row1.empty_columns = {1, 2}
        row2.empty_columns = {0, 1, 2, 3, 4, 5, 6}
        for i in (0, 3, 4, 5, 6):
            grid.visible_rows[i].row = row1
        for i in (7, 8, 9):
            grid.visible_rows[i].row = row2

        expected_row_empty_cols = set(range(2, 7))
        expected_height = grid.height - 1
        expected_visible_row_timestamps = [2, 2] +[0]*5 + [2]*3

        block = tetris.spawn_tetrimino("Z", 0)
        block.place_on_grid(grid)
        # check that height is correct
        assert grid.height == expected_height

        # check that the rows have the right columns empty
        row = grid.floor.next_row
        assert row.empty_columns == expected_row_empty_cols
        assert row.timestamp == 2

        # check that visibility is correct
        visible_row_timestamps = [row.timestamp for row in grid.visible_rows]
        assert visible_row_timestamps == expected_visible_row_timestamps