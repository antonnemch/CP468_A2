# CP468 — Sudoku as a CSP (Flat Structure)

This repository implements Sudoku as a **Constraint Satisfaction Problem (CSP)** with **AC-3** for arc consistency. If AC-3 does not fully solve a puzzle, a **backtracking search** (with optional heuristics) completes the solution. The structure is flat (no folders) except `test_puzzles/` for input grids, to simplify submission.

## Files

- **main.py** — CLI entry point. Orchestrates: read puzzle → build CSP → run AC-3 → if needed run backtracking → print solution/status.
- **sudoku_csp.py** — Defines the `CSP` object (variables, domains, neighbors, constraint) and `sudoku_csp_from_grid(grid)` factory.
- **constraints.py** — Binary Sudoku constraints and helpers (`binary_neq`, `same_row`, `same_col`, `same_box`).
- **ac3.py** — AC-3 solver (`ac3`, `revise`) with optional queue-length tracking.
- **backtracking.py** — Search-based solver when AC-3 doesn’t finish (supports MRV/LCV and forward-checking or AC-3 as inference). Includes a minimal `Trail` (undo stack).
- **heuristics.py** — Pluggable variable/value ordering heuristics (`select_var_mrv`, `order_values_lcv`, `degree_tiebreak`).
- **io_utils.py** — File I/O for Sudoku grids: `read_puzzle(path)`, `write_grid(path, grid)`.
- **printer_utils.py** — Pretty-printing and run status output: `print_grid(grid)`, `print_status(...)`.

## Puzzle format

- 9 lines × 9 characters per line  
- `1..9` for givens, `0` or `.` for blanks  
- Example: `530070000`

## Run (once implemented)

```bash
python main.py test_puzzles/puzzle1.txt --track-queue --show-queue
