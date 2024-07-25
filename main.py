import puzzles
from sudoku import SudokuGrid

if __name__ == '__main__':
    puzzle = SudokuGrid(puzzles.INKALA)
    print(puzzle)
    puzzle.solve()
    print(puzzle)