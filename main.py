def parse_input_string(input: str) -> list[list[int]]:
	print("Checking validity of input string...")
	if not isinstance(input, str):
		raise TypeError(f"Input should be of type string, but is type {type(input)}.")
	elif len(input) != 81:
		raise ValueError(f"Input string should have length 81, but has length {len(input)}.")
	elif not input.isdigit():
		raise ValueError(f"Input string should only contain digits.")
	else:
		print("All checks passed.")
		print("Parsing board from input...")
		board = []
		for i in range(0, len(input), 9):
			row = [int(c) for c in input[i:i+9]]
			board.append(row)
			print(row)
		print("Board successfully built.")
		return board
	
def find_an_empty_cell(board: list[list[int]]) -> tuple[int, int]:
	for row in range(9):
		for col in range(9):
			if board[row][col] == 0:
				return (row, col)
	return None

def find_canditates(board: list[list[int]], row: int, col: int) -> list[int]:
	'''Returns a list of numbers that don't occur in the same row, column, or 3x3 subgrid.'''
	valid_numbers = set(range(1,10))
	for i in range(9):
		valid_numbers.discard(board[row][i]) # check row
		valid_numbers.discard(board[i][col]) # check column
	# subgrid:
	sg_x_start = col // 3 * 3
	sg_y_start = row // 3 * 3
	for i in range(sg_x_start, sg_x_start + 3):
		for j in range(sg_y_start, sg_y_start + 3):
			valid_numbers.discard(board[j][i])
	return valid_numbers

def solve(board):
	empty_cell = find_an_empty_cell(board)
	if empty_cell is not None:	
		row, col = empty_cell
		candidates = find_canditates(board, row, col)
		for c in candidates:
			board[row][col] = c
			if solve(board) == True:
				return True
		board[row][col] = 0
	else:
		print("I think I've found the solution!")
		return True


if __name__ == "__main__":
	# represents a puzzle input. 0 means empty cell
	# read the string sequentially and fill in the sudoku grid from top to bottom and left to right
	input = "000260701680070090190004500820100040004602900050003028009300074040050036703018000"
	
	board = parse_input_string(input)
	solve(board)
	for row in board:
		print(row)