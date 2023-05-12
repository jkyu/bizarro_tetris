from simpletetris.grid import Grid
from simpletetris.tetrimino import IBlock, JBlock, LBlock, QBlock, SBlock, TBlock, ZBlock
from typing import List, Tuple
import sys
import argparse

def spawn_tetrimino(name: str, offset: int):
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
    return (tetris_input[0], int(tetris_input[1]))

def play_input_line(grid: Grid, input_line: List[Tuple[str, int]], verbose: bool = False):
    for block, offset in input_line:
        tetrimino = spawn_tetrimino(block, offset)
        tetrimino.place_on_grid(grid)
    return grid.height

def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action=argparse.BooleanOptionalAction, help="turn on to print out grid after each input line")
    args = parser.parse_args()

    grid = Grid()
    for line in sys.stdin:
        input_line = [parse_shape_and_left_offset(tetris_input) for tetris_input in line.split(",")]
        curr_stack_height = play_input_line(grid, input_line)
        print(curr_stack_height)
        if args.verbose:
            print(line.rstrip())
            grid.print_grid()