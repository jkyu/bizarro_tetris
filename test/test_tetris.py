from simpletetris import tetris
from simpletetris.grid import Grid

class TestTetris:
    def test_play_input_line_sequence1(self):
        test_sequence1 = [("I", 0), ("I", 4), ("Q", 8)]
        grid = Grid()
        assert tetris.play_input_line(grid, test_sequence1) == 1

    def test_play_input_line_sequence2(self):
        test_sequence2 = [("T", 1), ("Z", 3), ("I", 4)]
        grid = Grid()
        assert tetris.play_input_line(grid, test_sequence2) == 4

    def test_play_input_line_sequence3(self):
        test_sequence3 = [("Q", 0), ("I", 2), ("I", 6), ("I", 0), ("I", 6), ("I", 6), ("Q", 2), ("Q", 4)]
        grid = Grid()
        assert tetris.play_input_line(grid, test_sequence3) == 3