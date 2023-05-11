# Simple Tetris

Notes:
- don't need to bound the top of the grid
- don't need to consider horizontal movement of tetriminos
- grid is 10 spaces wide
- I should keep track of the current max height of each column and work out collisions when dropping a new piece
- STDOUT needs to report the height of my tetris stack after the sequence of moves
- need fast detection for completed lines. For a row, this can be a hash set containing the columns that are missing. The rationale for the negative status is that my experience playing tetris leads me to believe a dense board is more likely than a sparse board.
- for dealing with a downward shift of the board after clearing a line, I like the idea of a doubly linked list to store row status. There needs to be a good way to map the row to the row status though. Maybe we have a size 10 array that points to the current highest node for a given column. For any given tetrimino, we need to check all four points for possible collisions. We can optimize out some checks (like the pivot cell of an S-block). 
- When dropping a block, we only need to check current row and one row up or down, so I think a doubly linked list can support this.
- Need to handle dropping an S block in this scenario: --oooo
- For the doubly linked list solution, we can actually just return the length of the linked list for the final output in O(height) time.
- Alternatively, we can actually just deal with the 100x10 grid and do a shift of everything above a certain row using numpy. 


Tests required:
- ensure that a line is cleared properly