from typing import Callable


class Cell:
	def __init__(self, val: int, row: int, col: int) -> None:
		self.val = val
		self.row = row
		self.col = col
		self.candidates: set[int] = set()

class SudokuGrid:
	def __init__(self, input: str) -> None:
		self.verify_input(input)
		self.grid = self.build_grid(input)
		self.validate_grid()
		self.calculate_all_candidates()
		self.steps = 0
		print("Init complete.\n")

	def __str__(self) -> str:
		pretty = ""
		for row in self.grid:
			for col in row:
				pretty += str(col.val) + " "
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
		def has_duplicates(list_of_cells: list[Cell]) -> bool:
			seen = set()
			values = [cell.val for cell in list_of_cells]
			for val in values:
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
	
	def build_grid(self, input: str) -> list[list[Cell]]:
		print("Building sudoku puzzle grid from input...")
		puzzle: list[list[Cell]] = []
		for i in range(0, len(input), 9):
			row: list[Cell] = []
			for j in range(i, i + 9):
				row.append(Cell(val=int(input[j]), row=i//9, col=j%9))
			puzzle.append(row)
		print("Build successful.")
		return puzzle
	
	def find_empty_cell(self) -> Cell | None:
		'''Returns the first empty cell with the fewest candidates. Will return None if no empty cells are left, meaning the puzzle is solved.'''
		cell_with_fewest_candidates = None
		lowest_candidate_count = 10
		for row in range(9):
			for col in range(9):
				cell = self.grid[row][col]
				if cell.val == 0:
					cell_candidate_count = len(cell.candidates)
					if cell_candidate_count < lowest_candidate_count:
						cell_with_fewest_candidates = cell
						lowest_candidate_count = cell_candidate_count
		return cell_with_fewest_candidates
	
	def calculate_all_candidates(self):
		'''Fills in the candidates for all empty cells.'''
		print("Filling in candidates for all empty cells...")
		for row in range(9):
			for col in range(9):
				cell = self.grid[row][col]
				if cell.val == 0:
					candidates = self.find_candidates(row, col)
					cell.candidates.update(candidates)
		print("Done, all empty cells have their candidates filled in.")
	
	def find_candidates(self, row: int, col: int) -> set[int]:
		'''Returns a set of candidates for a given cell.'''
		candidates = set(range(1, 10))
		# check row and column:
		for i in range(9):
			candidates.discard(self.grid[row][i].val)
			candidates.discard(self.grid[i][col].val)
		# check 3x3 subgrid:
		subgrid_start_row = row // 3 * 3
		subgrid_start_col = col // 3 * 3
		for r in range(subgrid_start_row, subgrid_start_row + 3):
			for c in range(subgrid_start_col, subgrid_start_col + 3):
				candidates.discard(self.grid[r][c].val)
		return candidates
	
	def get_connected_cells(self, cell: Cell) -> set[Cell]:
		'''Returns a set containing all connected empty cells. Connected means in the same row, column, or 3x3 subgrid.'''
		cells: set[Cell] = set()
		row = cell.row
		col = cell.col
		for i in range(9):
			cells.add(self.grid[row][i])
			cells.add(self.grid[i][col])
		subgrid_start_row = row // 3 * 3
		subgrid_start_col = col // 3 * 3
		for r in range(subgrid_start_row, subgrid_start_row + 3):
			for c in range(subgrid_start_col, subgrid_start_col + 3):
				cells.add(self.grid[r][c])
		cells.remove(cell)
		cells = filter(lambda cell : cell.val == 0, cells)
		return set(cells)
	
	def get_connected_cells_with_candidate(self, cell: Cell, candidate: int) -> set[Cell]:
		'''Returns a set of connected empty cells that have the passed candidate in their candidate set.'''
		connected = self.get_connected_cells(cell)
		return set(filter(lambda cell : candidate in cell.candidates, connected))

	def backtrack(self) -> bool:
		target_cell = self.find_empty_cell()
		if target_cell is not None:
			for c in target_cell.candidates:
				target_cell.val = c
				connected_and_has_candidate = self.get_connected_cells_with_candidate(target_cell, c)
				for cell in connected_and_has_candidate:
					cell.candidates.discard(c)
				self.steps += 1
				if self.backtrack() == True:
					return True
				# probably something wrong here:
				for cell in connected_and_has_candidate:
					cell.candidates.add(c)
			target_cell.val = 0
		else:
			return True
	
	def solve(self):
		print("Solving puzzle...")
		if self.backtrack() == True:
			print("Found solution!")
			self.validate_grid()
			print(f"Puzzle solved in {self.steps} steps.")
		else:
			print("Unable to solve puzzle :(")