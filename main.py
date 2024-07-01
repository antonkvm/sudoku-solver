from sudoku import SudokuGrid
import puzzles

if __name__ == "__main__":
	sudoku = SudokuGrid(puzzles.SKIENA_HARD)
	sudoku.pretty_print()
	sudoku.solve()
	sudoku.pretty_print()