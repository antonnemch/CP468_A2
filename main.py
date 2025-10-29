"""
CP468 — main.py
Entry point and orchestration for Sudoku-as-CSP.

Contributors:
    - (Name 1)
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

Purpose:
    - Parse command-line arguments.
    - Read a Sudoku puzzle file into a 9x9 integer grid (0 = empty).
    - Build a CSP using sudoku_csp_from_grid(grid).
    - Run AC-3 to enforce arc-consistency.
    - Report whether the CSP is arc-consistent and solved.
    - If not solved, invoke the additional algorithm (backtracking search).
    - Print the final grid and optional AC-3 queue trace.

Expected Interfaces (to import/use):
    - io_utils.read_puzzle(path) -> List[List[int]]
    - sudoku_csp.sudoku_csp_from_grid(grid) -> CSP
    - ac3.ac3(csp, queue: Iterable[Arc] | None = None, track_queue: bool = False)
      -> tuple[bool, list[int] | None]
    - printer_utils.print_status(is_consistent: bool, solved: bool) -> None
    - printer_utils.print_grid(grid: List[List[int]]) -> None
    - Optional: backtracking.solve(csp) -> bool

CLI Arguments (to implement with argparse):
    - puzzle_path (positional): path to text file in the specified format.
    - --track-queue (flag): collect AC-3 queue length at each pop.
    - --show-queue (flag): print the collected queue lengths.

Contracts:
    - Must NOT mutate the input grid directly; CSP holds solver state.
    - May print intermediate info only behind flags.
    - Exit code remains 0 (assignment demo environment friendly).
"""
