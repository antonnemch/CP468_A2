"""
CP468 — io_utils.py
Reading and writing Sudoku puzzles & console printing helpers for grids and run status.

Contributors:
    - Anton Nemchinski


Functions:


    - def read_puzzle(path: str) -> list[list[int]]
        Format:
            - 9 lines × 9 characters.
            - '1'..'9' for givens.
            - '0' or '.' for blanks.
        Output:
            - 9×9 list of ints (0 for blank).
        Validation:
            - Assert 9 rows; each row has 9 valid characters.
    
    - def get_valid_puzzles() -> list[list[list[int]]]
        Behavior:
            - Returns a list of valid Sudoku puzzles.

    - def get_unsolvable_puzzles() -> list[list[list[int]]]
        Behavior:
            - Returns a list of unsolvable Sudoku puzzles.

    - def get_multiple_solution_puzzles() -> list[list[list[int]]]
        Behavior:
            - Returns a list of puzzles with multiple solutions.

    - def get_all_puzzles() -> list[list[list[int]]]
        Behavior:
            - Returns a combined list of all puzzles from the above three functions.    
    
    - def manual_input() -> list[list[int]]
        Behavior:
            - Prompts user to input a Sudoku puzzle line by line.
            - Validates input format as per read_puzzle.
            - Returns the constructed 9×9 grid.
    
    - def print_grid(grid: list[list[int]]) -> None
        Behavior:
            - Pretty-print the 9x9 grid.
            - Show '.' for 0.
            - Visual separators after cols 3 and 6, and rows 3 and 6.

    - def print_status(*, is_consistent: bool, solved: bool) -> None
        Behavior:
            - Print a concise standardized status line:
              "Arc-consistent: YES/NO | Solved: YES/NO"
"""

from pathlib import Path
from typing import List

def read_puzzle(path: str) -> list[list[int]]:
    grid = []
    with open(path, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 9, "Puzzle must have exactly 9 lines."
        for line in lines:
            line = line.strip()
            assert len(line) == 9, "Each line must have exactly 9 characters."
            row = []
            for char in line:
                if char in '123456789':
                    row.append(int(char))
                elif char in '0.':
                    row.append(0)
                else:
                    raise ValueError(f"Invalid character '{char}' in puzzle.")
            grid.append(row)
    return grid

def _puzzle_dir() -> Path:
    """Return absolute path to the test_puzzles directory."""
    return (Path(__file__).resolve().parent / "test_puzzles")

def _load_dir(dir_path: Path, label: str) -> List[List[List[int]]]:
    """
    Load every *.txt puzzle in a directory into grids using read_puzzle().
    Prints how many puzzles were found. Sorted by filename for deterministic order.
    """
    grids: List[List[List[int]]] = []
    if not dir_path.exists():
        print(f"[WARN] Directory not found: {dir_path}")
        return grids

    for f in sorted(dir_path.glob("*.txt")):
        if f.is_file():
            grids.append(read_puzzle(str(f)))

    print(f"[INFO] Loaded {len(grids):>2} {label} puzzle(s) from {dir_path.name}/")
    return grids


def get_valid_puzzles() -> List[List[List[int]]]:
    """
    Return list of grids from test_puzzles/valid/*.txt.
    Each grid is a 9x9 list[list[int]] with 0 for blanks.
    """
    return _load_dir(_puzzle_dir() / "valid", "valid")


def get_unsolvable_puzzles() -> List[List[List[int]]]:
    """
    Return list of grids from test_puzzles/unsolvable/*.txt.
    These should trigger inconsistency under AC-3 or search.
    """
    return _load_dir(_puzzle_dir() / "unsolvable", "unsolvable")


def get_unofficial_puzzles() -> List[List[List[int]]]:
    """
    Return list of 'unofficial' puzzles:
      - Solved puzzles (for regression/demo)
      - Multiple-solution puzzles (for robustness tests)
    """
    base = _puzzle_dir()
    solved = _load_dir(base / "solved", "solved")
    multi  = _load_dir(base / "multiple_solutions", "multiple-solution")
    return solved + multi


def get_all_puzzles() -> List[List[List[int]]]:
    """
    Convenience: return every available puzzle from all categories.
    """
    all_puzzles = (
        get_valid_puzzles()
        + get_unsolvable_puzzles()
        + get_unofficial_puzzles()
    )
    print(f"[INFO] Total puzzles loaded: {len(all_puzzles)}")
    return all_puzzles

def print_grid(grid: list[list[int]]) -> None:
    """
    Pretty-print the 9x9 grid.
    Show '.' for 0.
    Visual separators after cols 3 and 6, and rows 3 and 6.
    """
    for i, row in enumerate(grid):
        if i > 0 and i % 3 == 0:
            print(" - - - + - - - + - - -")
        row_str = ""
        for j, val in enumerate(row):
            if j > 0 and j % 3 == 0:
                row_str += " |"
            row_str += f" {val if val != 0 else '.'}"
        print(row_str)


def manual_input() -> list[list[int]]:
    """
    Prompt user to input a Sudoku puzzle line by line.
    Validates input format as per read_puzzle.
    Returns the constructed 9×9 grid.
    """
    print("Please enter your Sudoku puzzle line by line.")
    print("Use digits 1-9 for givens and 0 or . for blanks.")
    grid = []
    for i in range(9):
        while True:
            line = input(f"Line {i + 1}: ").strip()
            if len(line) != 9 or any(c not in '1234567890.' for c in line):
                print("Invalid input. Please enter exactly 9 characters using digits 1-9 and 0 or . for blanks.")
                continue
            row = [int(c) if c in '123456789' else 0 for c in line]
            grid.append(row)
            break
    print_grid(grid)
    return grid

def print_status(is_consistent: bool, solved: bool) -> None:
    """
    Print a concise standardized status line:
    "Arc-consistent: YES/NO | Solved: YES/NO"
    """
    consistent_str = "YES" if is_consistent else "NO"
    solved_str = "YES" if solved else "NO"
    print(f"Arc-consistent: {consistent_str} | Solved: {solved_str}")