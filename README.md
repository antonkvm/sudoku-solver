# Sudoku solver

Solve a Sudoku puzzle using backtracking and heuristics. I made this as a little personal challenge and because I play Sudoku on my phone a lot.

## Usage

~~~Python
from sudoku import SudokuGrid
import puzzles

# define a puzzle input:
grid_1 = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0],
]

# or choose a predefined one:
grid_2 = puzzles.NOTFUN

# create a new SudokuGrid object from the puzzle input:
puzzle = SudokuGrid(grid_1)

# show unsolved puzzle:
print(puzzle)

# solve it:
puzzle.solve()

# show solved puzzle:
print(puzzle)
~~~

## Implemented Heuristics

The program would work fine with just plain backtracking and the performance improvement is probably in the milliseconds, but I wanted to see how low I could push the number of backtracking steps by implementing these heuristics:

- Simple row, column, and 3x3 subgrid inconsistency check:
  - I can technically call this a heuristic because I check it at every step, not just at the end
- Minumum Remaining Values (MRV):
  - prefer trying a value for the cell with the fewest remaining candidates (i.e. most constrained)
  - a smaller candidate set to choose from reduces the chance of picking a wrong value
- Constraint Propagation:
  - entering a value into a cell removes that value from the candidate sets of connected cells
  - boosts effectiveness of MRV because we continuously reduce the size of candidate sets
- Look-Ahead Candidate Selection:
  - skip a candidate if choosing it would mean another cell has no valid canidate left through constraint propagation
  - effecting an empty candidate set means that backtracking branch is hopeless, so we can prune it
- Least Constraining Value (LCV)
  - prefer the candidate for a cell that impacts the fewest other candidate sets
  - reduces the chance of eliminating a correct candidate

## Performance

The program currently solves these puzzles (from `puzzles.py`) with this performace:

- easy1: 45 steps for 45 empty cells
- easy2: 45 steps for 45 empty cells
- intermediate: 834 steps for 57 empty cells
- difficult1: 2279 steps for 58 empty cells
- difficult2: 76 steps for 47 empty cells
- notfun: 3330 steps for 62 empty cells
- skiena_hard: 8522 steps for 64 empty cells

> A step is defined as trying out a value for a cell during backtracking.

## Solutions are not always deterministic

Many Sudoku puzzles have one valid solution, but counterintuitively, as puzzles get harder by having less pre-filled cells, the number of valid solutions increases. Think of how a puzzle with only one pre-filled cell would be extremely easy to solve, because for most cells you can enter whatever you want. That is why some puzzles that are considered to be the most challenging have more pre-filled cells than 'easier' ones.

## Heuristic trade-off

The performance generally improved when I added new heuristics and optimizations, but interestingly, adding the Least Constraining Value (LCV) Heuristic resulted in both better and worse performace, depending on the input puzzle. This demonstrates that implementing heuristics does not guarantee improved performance for every input, it just increases the chance of better performance.

| Optimization                | intermediate | difficult2 | notfun | skiena_hard |
|-----------------------------|:------------:|:----------:|:------:|:-----------:|
| Before adding LCV heuristic |      384     |     113    |  1230  |    27211    |
| After adding LCV heuristic  |      834     |     76     |  3330  |     8522    |

## Is backtracking dumb?

While totally effective, backtracking is really just mindless trial and error until we're lucky enough to stumble upon a valid solution. Adding heuristics into the mix makes it somewhat more intentional, but at it's core it's still a brute-force approach. To me that begs the questions wether it's more elegant to first go through all the cool tricks that exist to eliminate candidates for a cell (like pointing pairs, X-Wing, Swordfish, etc.), before eventually using backtracking only as a fallback.

## Puzzle sources

- SKIENA: Skiena, S. S. (2008). _The Algorithm Design Manual._ Springer Science & Business Media, 2 edition.
- INKALA: Dr. Arto Inkala
- All other: Fong, S., _Example Puzzles and Solutions_. Sudoku Sandiway. Retrieved September 18, 2023, from <https://sandiway.arizona.edu/sudoku/examples.html>

## Resources

- Blankertz, B. & Röhr, V., _Algorithmen und Datenstrukturen: Vorlesungsskript_. TU Berlin, Fachgebiet Neurotechnologie.
- Fong, S., _Heuristics_. Sudoku Sandiway. Retrieved September 16, 2023, from <https://sandiway.arizona.edu/sudoku/index.html#heuristics>
- Skiena, S. S. (2008). _The Algorithm Design Manual_. Springer Science & Business Media, 2 edition.
