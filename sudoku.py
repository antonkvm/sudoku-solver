class SudokuGrid:

	def __init__(self, input: str) -> None:
		self.verify_input(input)
		self.grid = self.build_puzzle(input)
		self.validate_grid()
		self.steps = 0
		print("Init complete.\n")

	def __str__(self) -> str:
		pretty = ""
		for row in self.grid:
			for col in row:
				pretty += str(col) + " "
			pretty += "\n"
		return pretty

	def verify_input(self, input: str):
		'''Raises an error if the input string is invalid in terms of type, length, or if it has non-digit elements.'''
		print("Verifying input...")
		if input == None:
			raise TypeError("Missing mandatory parameter: input string")
		elif not isinstance(input, str):
			raise TypeError(f"Input should be of type string, but is of type {type(input)}.")
		elif len(input) != 81:
			raise ValueError(f"Input string should have length 81, but has length {len(input)}.")
		elif not input.isdigit():
			raise ValueError(f"Input string should only contain digits.")
		else:
			print("All checks passed.")
	
	def validate_grid(self):
		'''Raises an error if the grid is invalid in terms of the sudoku rules.'''
		print("Checking grid validity in terms of sudoku rules...")
		def has_duplicates(l: list[int]) -> bool:
			seen = set()
			for val in l:
				if val == 0:
					continue
				elif val not in seen:
					seen.add(val)
				else:
					raise ValueError("Grid is invalid because a duplicate was found in a row, column, or 3x3 subgrid.")
		for i in range(9):
			has_duplicates(self.grid[i])
			has_duplicates([row[i] for row in self.grid])
			subgrid_values = []
			for j in range(9):
				row = (i // 3 * 3) + (j // 3)
				col = (i % 3 * 3) + (j % 3)
				subgrid_values.append(self.grid[row][col])
			has_duplicates(subgrid_values)
		print("Grid is valid.")
				
	def build_puzzle(self, input: str) -> list[list[int]]:
		print("Building sudoku puzzle from input...")
		puzzle = []
		for i in range(0, len(input), 9):
			row = [int(c) for c in input[i:i+9]]
			puzzle.append(row)
		print("Build successful.")
		return puzzle
	
	def find_empty_cell(self) -> tuple[int, int]:
		'''Find the first empty cell.'''
		for row in range(9):
			for col in range(9):
				if self.grid[row][col] == 0:
					return (row, col)
		# fallback for when puzzle is solved:
		return None
	
	def find_candidates(self, row: int, col: int) -> list[int]:
		'''Returns a list of candidates for a given cell.'''
		candidates = set(range(1, 10))
		# check row and column:
		for i in range(9):
			candidates.discard(self.grid[row][i])
			candidates.discard(self.grid[i][col])
		# check 3x3 subgrid:
		subgrid_start_row = row // 3 * 3
		subgrid_start_col = col // 3 * 3
		for r in range(subgrid_start_row, subgrid_start_row + 3):
			for c in range(subgrid_start_col, subgrid_start_col + 3):
				candidates.discard(self.grid[r][c])
		return candidates
	
	def reset_cell(self, row, col):
		'''Resets a cell to zero.'''
		self.grid[row][col] = 0

	def backtrack(self) -> bool:
		empty_cell = self.find_empty_cell()
		if empty_cell is not None:
			row, col = empty_cell
			candidates = self.find_candidates(row, col)
			for c in candidates:
				self.grid[row][col] = c
				self.steps += 1
				if self.backtrack() == True:
					return True
			self.reset_cell(row, col)
		else:
			return True
	
	def solve(self):
		print("Solving puzzle...")
		if self.backtrack() == True:
			print(f"Puzzle solved in {self.steps} steps.")
		else:
			print("Unable to solve puzzle :(")