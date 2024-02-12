# Sudoku solver

This application solves a given Sudoku puzzle using backtracking.

## Implemented Heuristics

Currently the app implements the following heuristics:

- simple row, column, and 3x3 subgrid inconsistency check
- Minumum Remaining Values (MRV):
  - prefer the cells with the fewest remaining candidates (i.e. the most constrained cells), reducing the chance of picking a wrong value
- Constraint Propagation:
  - entering a value into a cell removes that value from the candidate sets of connected cells
  - boosts effectiveness of MRV
- Look-Ahead Candidate Selection:
  - skip a candidate for a cell if choosing that value would cause another cell to be left with no candidates through constraint propagation
  - a cell with no candidates is a definite indication that a partial solution is wrong, meaning that branch can be pruned
  - Propably nullified by MRV, see explanation [here](#conflicting-heuristics).
- Least Constraining Value (LCV)
  - prefer the candidate for a cell that impacts the fewest candidate sets of other connected cells through constraint propagation, reducing the chance of eliminating a correct candidate

## Performance

The app currently solves these puzzles (from `puzzles.py`) with this performace:

- easy1: 45 steps for 45 empty cells
- easy2: 45 steps for 45 empty cells
- intermediate: 834 steps for 57 empty cells 
- difficult1: 2279 steps for 58 empty cells
- difficult2: 76 steps for 47 empty cells
- notfun: 3330 steps for 62 empty cells
- skiena_hard: 8522 for 64 empty cells

> A step is defined as entering a value into a cell and then moving on to the next cell.

Notice that for the easy puzzles, the algorithm never made a single wrong choice for a cell and never had to backtrack.

## Heuristic trade-off

The performance generally improved when I added new heuristics and optimizations, but interestingly, adding the Least Constraining Value Heuristic resulted in both better and worse performace, depending on the input puzzle. This shows that implementing a new heuristic is not a guaranteed improvement for every input, but rather just increases the chance of improvement.

| Optimization                | intermediate | difficult2 | notfun | skiena_hard |
|-----------------------------|:------------:|:----------:|:------:|:-----------:|
| Before adding LCV heuristic |      384     |     113    |  1230  |    27211    |
| After adding LCV heuristic  |      834     |     76     |  3330  |     8522    |

## Puzzle sources

- Fong, S., _Example Puzzles and Solutions_. Sudoku Sandiway. Retrieved September 18, 2023, from https://sandiway.arizona.edu/sudoku/examples.html
- Skiena, S. S. (2008). _The Algorithm Design Manual._ Springer Science & Business Media, 2 edition.

## Conflicting Heuristics

I would argue that the MRV heuristic nullifies any effect the Look-Ahead Candidated Selection heuristic would have, for the following reason:

Look-Ahead Candidate Selection skips a candidate for a cell (A), if choosing it would cause a seperate cell (B) to be left with no candidates, because there is no way that a solution can be found for that case. But in this scenario, cell A has more candidates than cell B — meaning MRV would have selected cell B before cell A anyway and Look-Ahead Candidate Selection would never take effect.

## A different approach?

Backtracking is – while definitely effective – a somewhat 'dumb' way of solving a sudoku puzzle, because it's basically just trial and error with some optimizations. Because most puzzles are solveable by humans, their solution can be deduced by repeatedly eliminating cell candidates using different techniques (like hidden pairs, pointing pairs, etc) until we find an definite solution for every cell. This is a more elegant approach, which is why I think it would be smart to implement these constraint propagation methods for eliminating candidates as a primary solving agent, while demoting the brute-force backtracking appraoch to a fallback method, for when candidate elimination hits a dead end.

## Resources

- Blankertz, B. & Röhr, V., _Algorithmen und Datenstrukturen: Vorlesungsskript_. TU Berlin, Fachgebiet Neurotechnologie.
- Fong, S., _Heuristics_. Sudoku Sandiway. Retrieved September 16, 2023, from https://sandiway.arizona.edu/sudoku/index.html#heuristics
- Skiena, S. S. (2008). _The Algorithm Design Manual_. Springer Science & Business Media, 2 edition.