import puzzles
from sudoku import SudokuGrid

if __name__ == '__main__':
    sudoku = SudokuGrid(puzzles.SKIENA_HARD)
    sudoku.pretty_print()
    sudoku.solve()
    sudoku.pretty_print()
