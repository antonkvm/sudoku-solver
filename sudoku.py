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

	def print(self) -> str:
		'''Prints the grid in a single line string.'''
		string = ""
		for row in self.grid:
			for cell in row:
				string += str(cell.val)
		print(string)
	
	def pretty_print(self) -> None:
		'''Prints the grid in a pretty way.'''
		pretty = ""
		for row in self.grid:
			for col in row:
				pretty += str(col.val) + " "
			pretty += "\n"
		print(pretty)
	
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
	
	# TODO: having this grid and also storing the row/col in the cell object is kinda redundant.
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
	
	def calculate_all_candidates(self):
		'''Fills in the candidates for all empty cells.'''
		print("Filling in candidates for all empty cells...")
		for row in range(9):
			for col in range(9):
				cell = self.grid[row][col]
				if cell.val == 0:
					candidates = self.find_candidates(row, col)
					cell.candidates.update(candidates)
		print("Done.")

	def find_candidates(self, row: int, col: int) -> set[int]:
		'''Returns a set of candidates for a given cell.'''
		candidates = set(range(1, 10))
		cell = self.grid[row][col]
		cells = self.get_connected_cells(cell)
		for c in cells:
			candidates.discard(c.val)
		return candidates

	def find_empty_cell(self) -> Cell | None:
		'''Returns the first empty cell with the smallest, non-empty candidate set. Will return None if none are found.'''
		cell_with_fewest_candidates = None
		lowest_candidate_count = 10
		for row in range(9):
			for col in range(9):
				cell = self.grid[row][col]
				if cell.val == 0:
					cell_candidate_count = len(cell.candidates)
					if cell_candidate_count < lowest_candidate_count and cell_candidate_count > 0:
						cell_with_fewest_candidates = cell
						lowest_candidate_count = cell_candidate_count
		return cell_with_fewest_candidates
	
	def get_connected_cells(self, cell: Cell) -> set[Cell]:
		'''Returns a set of all connected cells, empty or not.'''
		cells: set[Cell] = set()
		row = cell.row
		col = cell.col
		for i in range(9):
			cells.add(self.grid[row][i])
			cells.add(self.grid[i][col])
		sector_start_row = row // 3 * 3
		sector_start_col = col // 3 * 3
		for r in range(sector_start_row, sector_start_row + 3):
			for c in range(sector_start_col, sector_start_col + 3):
				cells.add(self.grid[r][c])
		cells.remove(cell)
		return cells
	
	def get_connected_empty_cells(self, cell: Cell) -> set[Cell]:
		'''Returns a set containing all connected empty cells. Connected means in the same row, column, or 3x3 subgrid.'''
		cells = self.get_connected_cells(cell)
		cells = filter(lambda cell : cell.val == 0, cells)
		return set(cells)
	
	def get_propagation_targets(self, cell: Cell, candidate: int) -> set[Cell]:
		'''Returns a set of empty cells that are connected to the passed cell and have the passed candidate in their candidate set.'''
		connected = self.get_connected_empty_cells(cell)
		return set(filter(lambda cell : candidate in cell.candidates, connected))
	
	def solution_found(self) -> True:
		'''Returns True if the grid contains no empty cells and no sudoku rules are broken.'''
		for row in self.grid:
			for cell in row:
				if cell.val == 0:
					return False
		print("Solution found.")
		self.validate_grid()
		print(f"Took {self.steps} steps.")
		return True
	
	def sort_candidates(self, cell: Cell) -> list[int]:
		'''Returns a list of candidate integers that is sorted by the number of cells that would have their candidate sets affected through constraint propagation if that candidate is chosen. In other words, the first candidate in the returned list is the candidate that will affect the fewest other cell candidate sets. Used for LCV heuristic.'''
		candidates = cell.candidates
		candidates = list(candidates)
		candidates.sort(key=lambda c : len(self.get_propagation_targets(cell, c)))
		return candidates

	def backtrack(self):
		# exit condition:
		if not self.solution_found():
			# select most constrained cell with (Minimum Remaining Value):
			target_cell = self.find_empty_cell()
			# sort candidates by impact on other cells (Least Constraining Value):
			sorted_candidates = self.sort_candidates(target_cell)
			for c in sorted_candidates:
				propagation_targets = self.get_propagation_targets(target_cell, c)
				# look-ahead candidate selection:
				if {c} in [pt.candidates for pt in propagation_targets]:
					continue
				# constraint propagation:
				for pt in propagation_targets:
					pt.candidates.discard(c)
				# execute step:
				target_cell.val = c
				self.steps += 1
				# go to next step:
				if self.backtrack():
					return True
				# undo step:
				target_cell.val = 0
				for pt in propagation_targets:
					pt.candidates.add(c)
		else:
			# solution found:
			return True

	def solve(self):
		print("Solving puzzle...")
		if self.backtrack() != True:
			print("Unable to solve puzzle :(")