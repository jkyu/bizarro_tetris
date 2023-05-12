# Simple Tetris

## Running the tetris engine
Running the tetris engine requires installing it as a python package. In the same directory as this README, run:
```
pip install .
```

Once installed, the program can be executed using the `tetris` command. As specified in the prompt, the program takes `STDIN` and writes its output to `STDOUT`. Obtain the output file by running:
```
tetris < input.txt > output.txt
```

By default, verbose mode is off so as to not interfere with validation. However, the user can inspect the tetris grid visually after each input line by using the `--verbose` flag.

## Testing
A test suite leveraging `pytest` is included here to verify that the components of the simplified tetris engine run correctly.
To run the test suite, enter the command:
```
pytest
```
in the same directory as this README.

## Design decisions
It is possible that the reader may find the choice to represent the tetris grid as a doubly linked list of rows to be interesting.
The more obvious choice of representation would be an array-based solution, like a list of lists, for example. 
I wanted to explore the doubly linked list solution because of several advantages that I would like to justify here.
Most notably, a row can be removed from the grid in constant time and memory by dropping the row from the linked list.
This makes the removal of low rows really nice, especially if there is a large stack above the cleared row.
The array-based approaches have a weakness in this regard.
Options for excising a cleared row with an array-based implementation include:
- making a new outer list that excludes cleared row, e.g., by slicing and then concatenating to remove the cleared row. This incurs the cost of traversing all rows to build a new list and the memory cost of allocating all rows to the new outer list.
- moving the tetris stack one unit down, which incurs the cost modifying all of the rows above the cleared row. This gets worse if the cleared row is lower in the tetris stack.

Compared to the linked list solution, the array-based solution takes a hit in memory or grid traversal (or both) when removing a cleared line. In all fairness, these drawbacks would not be noticeable because of the small scale of this problem, where the stack height is not expected to exceed 100 rows and the grid width is fixed to 10 columns. Additionally, while frequent removal of low rows would be common in a standard tetris game (e.g., ["n-wide" combo setups](https://harddrop.com/wiki/Combo_Setups) or the stacking strategy of leaving one column open for 4-line clears with the vertical I-block), it became clear after a few examples that most cleared lines in this simplified tetris version come near the top of the stack since blocks cannot be rotated. This reduces the savings afforded by the doubly linked list design (though row removals are still constant memory!).

The doubly linked list solution does come with some drawbacks. 
The most obvious is the added complexity of the implementation, especially with the bookkeeping required to maintain an index of the "visible rows."
A "visible row" refers to a row that I could see if I looked straight down into the tetris stack from the top.
These are the rows that are candidates for collisions with newly spawned tetris blocks.

In the below example, `x` indicates an occupied cell that is also in the "visible row" for that column, `o` represents an occupied cell in the grid, and `-` represents an empty cell. 
Note that if there is no `x` in a column, the "visible row" is the bottom of the tetris grid (termed the "floor" in this project).
The number to the left is the row number and the numbers on the bottom number the columns.
```
3|xxxxxxx---|
2|----oo----|
1|--ooo---x-|
 |0123456789| <- floor
```
If we remove row 3 with a `T7` input, the "visible rows" index must be updated.
The updated grid would appear as:
```
2|----xx----|
1|--xxo---x-|
 |0123456789| <- floor
```
I believe the array-based solution may have a similar bookkeeping problem if we want to avoid finding collisions for a block on its way down from the top of the grid.
Thankfully, I have a bunch of tests to show that bookkeeping for the linked list solution is handled properly.

A second drawback is the additional memory overhead of making each row a linked list node instead of an array, but this is the tradeoff for reducing the memory cost of row removal.

The third drawback is that the linked list solution would not work well in a dynamic tetris implementation, where a block falls one cell per time interval. 
An array-based grid would be preferable there to handle motion of the falling block (and then maybe the stack shifting due to cleared lines doesn't sound so bad).
The static nature of this simplified tetris engine changes a lot about how the problem can be interpreted.

To conclude, I thought this was an interesting idea to explore, and I hope you feel the same way.
Thanks for reading!
