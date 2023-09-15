# Sudoku solver

This programm solves a given Sudoku puzzle.

As of right now it implements a backtracking algorithm that uses only very simple heuristics, and is therefore pretty limited in it's capabilites at solving more difficult puzzle inputs. In the future, I plan on implementing more sophisticated heuristics to improve it's it's efficiency and maybe add a frontend to it.

## Implemented Heuristics

Currently the app only checks for simple row, column or subgrid inconsistency when building a candidate list for a given cell, as explained [here](https://sandiway.arizona.edu/sudoku/inconsistency.html).

## Next steps

The next improvements that make sense to implement are for instance:

 - row, column and 3x3 insufficiency ([read more](https://sandiway.arizona.edu/sudoku/insufficiency.html))
 - row, column and 3x3 cover elemination ([read more](https://sandiway.arizona.edu/sudoku/cover.html))
 - smarter cell selection: when choosing the next cell to fill, prefer the one with the least candidates
 - other tricks one might use when solving a sudoku puzzle manually

## Resources

- "Algorithmen und Datenstrukturen: Vorlesungsskript", Benjamin Blankertz und Vera Röhr (Fachgebiet Neurotechnologie, TU Berlin)
- [Sudoku Sandiway](https://sandiway.arizona.edu/sudoku/), Sandiway Fong (Department of Linguistics and Department of Computer Science University of Arizona)
  - input puzzle sourced from [here](https://sandiway.arizona.edu/sudoku/examples.html)