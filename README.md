# Sudoku solver

This application solves a given Sudoku puzzle using backtracking.

## Implemented Heuristics

Currently the app implements the following heuristics:

- simple row, column, and 3x3 subgrid inconsistency check
- Minumum Remaining Values (MRV): prefer the cells with the fewest remaining candidates, reducing chance of picking a wrong value
- Constraint Propagation: entering a value into a cell removes that value from the candidate sets of connected cells

## Performance

The app solves these puzzles (from `puzzles.py`) with this performace:

- easy1: 45 steps for 45 empty cells
- easy2: 45 steps for 45 empty cells
- intermediate: 421 steps for 57 empty cells 
- difficult1: 5995 steps for 58 empty cells
- difficult2: 117 steps for 47 empty cells
- notfun: 1369 steps for 62 empty cells
- skiena_hard: 33041 steps for 64 empty cells

Notice that for the easy puzzles, the algorithm never made a single wrong choice for a cell and never had to backtrack. It's also evident that the difficulty of a puzzle is not just dependent on the number of empty cells, as the puzzle 'notfun' was solved faster than 'difficult1', even though it has more empty cells.

## Puzzle sources

Fong, S., _Example Puzzles and Solutions_. Sudoku Sandiway. Retrieved September 18, 2023, from https://sandiway.arizona.edu/sudoku/examples.html

Skiena, S. S. (2008). _The Algorithm Design Manual._ Springer Science & Business Media, 2 edition.

## Next steps

The next improvements that make sense to implement are for instance:

 - row, column and 3x3 cover elemination ([read more](https://sandiway.arizona.edu/sudoku/cover.html))
 - Least Constraining Value (LCV): select the candidate for a cell that impacts the fewest candidate sets of connected cells, reducing the chance of eliminating a correct candidate
 - Other various tricks one might use when solving a sudoku puzzle manually, for example:
   - candidate uniqueness -> when a candidate only occurs once in a row/column/subgrid, it can be entered directly
   - obvious pairs/triples --> when 2 or 3 cells contain exactly 2 or 3 unique candidates, these candidates must occur in this group of cells and can be removed from any other cell connected to that group
   - hidden pairs/triples --> when a set of candidate values only occur in a same-sized set of cells inside a subgrid, column or row, any other candidates in these cells can be eliminated
   - pointing pairs/triples --> when a candidate value only occurs in 2 or 3 cells of the same subgrid, and these cells are in a straight line, they eliminate this candidate from any cells that they 'point' at
   - X-Wing
   - Y-Wing

## Resources

- Blankertz, B. & Röhr, V., _Algorithmen und Datenstrukturen: Vorlesungsskript_. TU Berlin, Fachgebiet Neurotechnologie.
- Fong, S., _Heuristics_. Sudoku Sandiway. Retrieved September 16, 2023, from https://sandiway.arizona.edu/sudoku/index.html#heuristics