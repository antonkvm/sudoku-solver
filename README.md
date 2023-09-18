# Sudoku solver

This application solves a given Sudoku puzzle using backtracking.

## Implemented Heuristics

Currently the app implements the following heuristics:

- simple row, column, and 3x3 subgrid inconsistency check
- Minumum Remaining Values (MRV):
  - prefer the cells with the fewest remaining candidates (i.e. the most constrained cells), reducing the chance of picking a wrong value
- Constraint Propagation:
  - entering a value into a cell removes that value from the candidate sets of connected cells
  - facilitates the effectiveness of MRV
- Look-ahead candidate selection:
  - skip a candidate for a cell if choosing that value would cause another cell to have an empty candidate set through constraint propagation
  - that candidate is hopeless because eventually, we would encounter that other candidateless cell and would have to backtrack

## Performance

The app solves these puzzles (from `puzzles.py`) with this performace:

- easy1: 45 steps for 45 empty cells
- easy2: 45 steps for 45 empty cells
- intermediate: 384 steps for 57 empty cells 
- difficult1: 5559 steps for 58 empty cells
- difficult2: 113 steps for 47 empty cells
- notfun: 1230 steps for 62 empty cells
- skiena_hard: 27211 steps for 64 empty cells

A step is defined as entering a value into a cell and then moving on to the next cell.

Notice that for the easy puzzles, the algorithm never made a single wrong choice for a cell and never had to backtrack. It's also evident that the difficulty of a puzzle is not just dependent on the number of empty cells, as the puzzle 'notfun' was solved faster than 'difficult1', even though it has more empty cells.

## Puzzle sources

Fong, S., _Example Puzzles and Solutions_. Sudoku Sandiway. Retrieved September 18, 2023, from https://sandiway.arizona.edu/sudoku/examples.html

Skiena, S. S. (2008). _The Algorithm Design Manual._ Springer Science & Business Media, 2 edition.

## Next steps

The next improvements that make sense to implement are for instance:

 - row, column and 3x3 cover elemination ([read more](https://sandiway.arizona.edu/sudoku/cover.html))
 - Least Constraining Value (LCV): select the candidate for a cell that impacts the fewest candidate sets of connected cells, reducing the chance of eliminating a correct candidate
 - Other various tricks one might use when solving a sudoku puzzle manually

## Resources

- Blankertz, B. & Röhr, V., _Algorithmen und Datenstrukturen: Vorlesungsskript_. TU Berlin, Fachgebiet Neurotechnologie.
- Fong, S., _Heuristics_. Sudoku Sandiway. Retrieved September 16, 2023, from https://sandiway.arizona.edu/sudoku/index.html#heuristics
- Skiena, S. S. (2008). _The Algorithm Design Manual_. Springer Science & Business Media, 2 edition.