from simpletetris.grid import Grid
from simpletetris.row import Row
from simpletetris.tetrimino import IBlock, JBlock, LBlock, QBlock, SBlock, TBlock, ZBlock
from typing import List, Tuple
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

# test_sequence = ["I0", "I4", "Q8"]
# test_sequence = ["T1","Z3","I4"]
# test_sequence = ["Q0","I2","I6","I0","I6","I6","Q2","Q4"]
# grid = Grid()
# for block in test_sequence:
#     tetrimino = spawn_tetrimino(block[0], int(block[1]))
#     tetrimino.place_on_grid(grid)
#     grid.print_grid()

def read_input_file(file_name: str) -> List[List[str]]:
    with open(file_name, "r") as input_file:
        input_lines = [[parse_shape_and_left_offset(tetris_input) for tetris_input in line.split(",")] for line in input_file]
        return input_lines

def parse_shape_and_left_offset(tetris_input: str) -> Tuple[str, int]:
    return (tetris_input[0], int(tetris_input[1]))

def play_simplified_tetris(input_file:str):
    block_sequences = read_input_file(input_file)
    grid = Grid()
    for input_line in block_sequences:
        for block, offset in input_line:
            tetrimino = spawn_tetrimino(block, offset)
            # print("timestamp", [x.row.timestamp for x in grid.visible_rows if isinstance(x.row, Row)])
            tetrimino.place_on_grid(grid)
        print(input_line)
        grid.print_grid()

if __name__=="__main__":
    play_simplified_tetris(sys.argv[1])