from sudoku import SudokuGrid
import puzzles

if __name__ == "__main__":
	sudoku = SudokuGrid(puzzles.SKIENA_HARD)
	# invalid = SudokuGrid(puzzles.INVALID)
	sudoku.solve()
	# sudoku.pretty_print()