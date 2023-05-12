import argparse
import sys
from typing import List, Tuple

from simpletetris.grid import Grid
from simpletetris.tetrimino import (
    IBlock,
    JBlock,
    LBlock,
    QBlock,
    SBlock,
    TBlock,
    ZBlock,
)


def spawn_tetrimino(name: str, offset: int):
    """Return the correct block with its column offset."""
    match name:
        case "I":
            return IBlock(offset)
        case "J":
            return JBlock(offset)
        case "L":
            return LBlock(offset)
        case "Q":
            return QBlock(offset)
        case "S":
            return SBlock(offset)
        case "T":
            return TBlock(offset)
        case "Z":
            return ZBlock(offset)


def parse_shape_and_left_offset(tetris_input: str) -> Tuple[str, int]:
    """
    Split the input string, e.g. Q4, into a tuple of the block name and offset.
    """
    return (tetris_input[0], int(tetris_input[1]))


def play_input_line(grid: Grid, input_line: List[Tuple[str, int]]):
    """Perform a sequence of block placements onto the grid."""
    for block_name, offset in input_line:
        tetrimino = spawn_tetrimino(block_name, offset)
        tetrimino.place_on_grid(grid)
    return grid.height


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        "-v",
        action=argparse.BooleanOptionalAction,
        help="turn on to print out grid after each input line",
    )
    args = parser.parse_args()

    for line in sys.stdin:
        grid = Grid()
        input_line = [
            parse_shape_and_left_offset(tetris_input)
            for tetris_input in line.split(",")
        ]
        curr_stack_height = play_input_line(grid, input_line)
        if args.verbose:
            print(line.rstrip())
            grid.print_grid()
        print(curr_stack_height)
