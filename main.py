from sudoku import SudokuGrid
import puzzles

if __name__ == "__main__":
	sudoku = SudokuGrid(puzzles.EASY)
	sudoku.validate()
	invalid = SudokuGrid(puzzles.INVALID)
	invalid.validate()
	# sudoku.solve()
	# sudoku.validate()
