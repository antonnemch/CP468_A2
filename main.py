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


def demo_io() -> None:
    """
    Demo for I/O and pretty printing (no solving yet).
    - Reads and prints puzzles category by category.
    - Shows placeholder status for each puzzle.
    - Runs one manual input session at the end.
    """
    from io_utils import (
        get_valid_puzzles, get_unsolvable_puzzles,
        get_unofficial_puzzles, manual_input, print_grid)
    
    categories = [
        ("VALID", get_valid_puzzles),
        ("UNSOLVABLE", get_unsolvable_puzzles),
        ("UNOFFICIAL (solved + multiple-solution)", get_unofficial_puzzles),
    ]

    print("\n=== CP468 Sudoku I/O Demo ===")
    for label, loader in categories:
        print(f"\n--- {label} ---")
        try:
            puzzles = loader()
        except Exception as e:
            print(f"[ERROR] Failed to load {label.lower()} puzzles: {e}")
            continue

        if not puzzles:
            print(f"[INFO] No {label.lower()} puzzles found.")
            continue

        for idx, grid in enumerate(puzzles, start=1):
            print(f"\n[{label}] Puzzle {idx}/{len(puzzles)}")
            print_grid(grid)
            # Placeholder status (solver not wired yet)
            print("Arc-consistent: N/A | Solved: N/A  (placeholder)")

    # Manual input mode
    print("\n=== Manual Input Mode ===")
    user_grid = manual_input()
    print("Arc-consistent: N/A | Solved: N/A  (placeholder)")
    print("\n=== End of I/O Demo ===")


if __name__ == "__main__":
    demo_io()