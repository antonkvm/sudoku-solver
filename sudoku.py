class Cell:
    def __init__(self, val: int, row: int, col: int) -> None:
        self.val = val
        self.row = row
        self.col = col
        self.candidates: set[int] = set()


def has_duplicates(cells: list[Cell]) -> bool:
    filled_cells = [c for c in cells if c.val != 0]
    return len(filled_cells) != len(set(filled_cells))


class SudokuGrid:
    def __init__(self, input: list[list[int]]) -> None:
        self.verify_input(input)
        self.grid = self.make_cells(input)
        self.verify_rules()
        self.populate_candidate_sets()
        self.steps = 0

    def __str__(self) -> str:
        s = ''
        h_div = ('+' + '-' * 7) * 3 + '+'
        for i, row in enumerate(self.grid):
            if i % 3 == 0:
                s += h_div + '\n'
            row_vals = [cell.val if cell.val != 0 else ' ' for cell in row]
            row_str = ''
            for j, val in enumerate(row_vals):
                if j % 3 == 0:
                    row_str += '|'
                row_str += str(val)
            row_str += '|'
            row_str = ' '.join(row_str)
            s += row_str + '\n'
        s += h_div
        return s

    def verify_input(self, input):
        if not isinstance(input, list):
            raise TypeError(f'Input should be of type list but is of type {type(input)}')
        if len(input) != 9:
            raise ValueError(f'Input list should contain 9 elements but actually contains {len(input)}.')
        for sublist in input:
            if not isinstance(sublist, list):
                raise TypeError(f'Input should be a list of lists but contains an element of type {type(sublist)}.')
            if len(sublist) != 9:
                raise ValueError(f'Input sublists should be of length 9 but but actually is of length {len(sublist)}.')
            for item in sublist:
                if not isinstance(item, int):
                    raise TypeError(f'All elements of sublists should integers, but found one of type {type(item)}.')

    def make_cells(self, input: list[list[int]]) -> list[list[Cell]]:
        """Convert the list of lists of integers to a list of lists of Cell objects."""
        grid = []
        for i, row in enumerate(input):
            grid_row = []
            for j, val in enumerate(row):
                cell = Cell(val, row=i, col=j)
                grid_row.append(cell)
            grid.append(grid_row)
        return grid

    def verify_rules(self):
        """Raise an error if the puzzle grid breaks a sudoku rule."""
        # Loop 9 times, verifying one row, column and subgrid in each loop:
        for i in range(9):
            row_vals = self.grid[i]
            col_vals = [row[i] for row in self.grid]
            subgrid_vals = []
            for j in range(9):
                sg_row = (i // 3 * 3) + (j // 3)
                sg_col = (i % 3 * 3) + (j % 3)
                subgrid_vals.append(self.grid[sg_row][sg_col])
            if has_duplicates(row_vals):
                raise ValueError(f'Grid is invalid because row {i+1} (from the top) has a duplicate.')
            if has_duplicates(col_vals):
                raise ValueError(f'Grid is invalid because column {i+1} (from the left) has a duplicate.')
            if has_duplicates(subgrid_vals):
                raise ValueError(f'Grid is invalid because subgrid {i+1} () has a duplicate.')

    def populate_candidate_sets(self):
        """Fills in the candidates for all empty cells."""
        for row in self.grid:
            for cell in row:
                if cell.val == 0:
                    candidates = self.find_candidates(cell)
                    cell.candidates.update(candidates)

    def find_candidates(self, cell: Cell) -> set[int]:
        candidates = set(range(1, 10))
        cells = self.get_connected_cells(cell)
        for c in cells:
            candidates.discard(c.val)
        return candidates

    def get_connected_cells(self, cell: Cell) -> set[Cell]:
        """Returns a set of all connected cells, empty or not."""
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
        cells.remove(cell)  # remove self
        return cells

    def get_most_constrained_cell(self) -> Cell | None:
        """Return the cell with the smallest candidate set."""
        empty_cells = [cell for row in self.grid for cell in row if cell.val == 0]
        sorted_cells = sorted(empty_cells, key=lambda cell: len(cell.candidates))
        return sorted_cells[0]

    def get_propagation_targets(self, cell: Cell, candidate: int) -> set[Cell]:
        """Return the set of empty cells connected to `cell` that have `candidate` in their candidate set."""
        connected = self.get_connected_cells(cell)
        return {cell for cell in connected if cell.val == 0 and candidate in cell.candidates}  # set comprehension

    def solution_found(self) -> True:
        """Return True if the grid contains no empty cells and no sudoku rules are broken."""
        for row in self.grid:
            for cell in row:
                if cell.val == 0:
                    return False
        print('Solution found.')
        self.verify_rules()
        print(f'Took {self.steps} steps.')
        return True

    def sort_candidates_by_propagation_impact(self, cell: Cell) -> list[int]:
        """
        Return the candidates of the passed cell as a list sorted by the number of other empty cells that would have
        their candidate set affected if that candidate was chosen.
        """
        candidates = list(cell.candidates)
        return sorted(candidates, key=lambda candidate: len(self.get_propagation_targets(cell, candidate)))

    def backtrack(self):
        if not self.solution_found():  # exit condition
            target_cell = self.get_most_constrained_cell()
            sorted_candidates = self.sort_candidates_by_propagation_impact(target_cell)
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
            return True  # solution found

    def solve(self):
        print('Solving puzzle...')
        if self.backtrack() is not True:
            print('Unable to solve puzzle :(')
