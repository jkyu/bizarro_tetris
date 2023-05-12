from simpletetris.grid import Grid
from simpletetris.row import Row
from simpletetris.tetrimino import IBlock, JBlock, LBlock, QBlock, SBlock, TBlock, ZBlock
from typing import List, Tuple
import argparse
import sys

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

def play_simplified_tetris(input_file: str, output_file: str, verbose: bool):
    grid = Grid()
    with open(output_file, "w") as out_file:
        with open(input_file, "r") as in_file:
            for line in in_file:
                input_line = [parse_shape_and_left_offset(tetris_input) for tetris_input in line.split(",")]
                curr_stack_height = play_input_line(grid, input_line)
                out_file.write(str(curr_stack_height))
                if verbose:
                    print(line.rstrip())
                    grid.print_grid()

def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, help="path to input.txt file containing tetris inputs")
    parser.add_argument("--output", "-o", type=str, help="name of output file in which to write results")
    parser.add_argument("--verbose", "-v", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    play_simplified_tetris(args.input, args.output, args.verbose)