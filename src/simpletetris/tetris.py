from simpletetris.grid import Grid
from simpletetris.tetrimino import IBlock, JBlock, LBlock, QBlock, SBlock, TBlock, ZBlock

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
test_sequence = ["Q0","I2","I6","I0","I6","I6","Q2","Q4"]
grid = Grid()
for block in test_sequence:
    tetrimino = spawn_tetrimino(block[0], int(block[1]))
    tetrimino.place_on_grid(grid)
    print(grid.height)
grid.print_grid()
