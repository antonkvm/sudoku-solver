from sudoku import SudokuGrid
import puzzles

if __name__ == "__main__":
	sudoku = SudokuGrid(puzzles.HARD)
	# invalid = SudokuGrid(puzzles.INVALID)
	sudoku.solve()
	print(sudoku)