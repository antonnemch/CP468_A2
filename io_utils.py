"""
CP468 - io_utils.py
Reading and writing Suduoku puzzles

Author: Anton Nemchinski
"""


from pathlib import Path
from typing import List

def read_puzzle(path: str) -> list[list[int]]:
    """
    Read a Sudoku puzzle from a text file
    Return it as a 9x9 list of integers
    """

    grid = []
    with open(path, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 9, "Puzzle must have exactly 9 lines."
        for line in lines:
            line = line.strip()
            assert len(line) == 9, " make sure each line must have exactly 9 characters."
            row = []
            for char in line:
                # Convert digits 1–9 to integers and treat '0' or '.' as blanks
                if char in '123456789':
                    row.append(int(char))
                elif char in '0.':
                    row.append(0)
                else:
                    raise ValueError(f"Invalid character '{char}' in puzzle.")
            grid.append(row)

    return grid


def _puzzle_dir() -> Path:
    # Return absolute path to the test_puzzles directory.
    return (Path(__file__).resolve().parent / "test_puzzles")

def _load_dir(dir_path: Path, label: str) -> List[List[List[int]]]:
    """
    Load all puzzles from a folder using read_puzzle()
    Print how many puzzles were found. Sorted by filename for deterministic order.
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
    Return list of valid Sudoku puzzles from test_puzzles/valid/*.txt.
    """

    return _load_dir(_puzzle_dir() / "valid", "valid")


def get_unsolvable_puzzles() -> List[List[List[int]]]:
    """
    Return list of unsolavable Sudoku puzzles from test_puzzles/unsolvable/*.txt.
    Should trigger inconsistency under AC-3 or search.
    """

    return _load_dir(_puzzle_dir() / "unsolvable", "unsolvable")


def get_unofficial_puzzles() -> List[List[List[int]]]:
    """
    Load solved and multiple-solution puzzles
    Return unofficial puzzles
    """

    base = _puzzle_dir()
    solved = _load_dir(base / "solved", "solved")
    multiple_solutions  = _load_dir(base / "multiple_solutions", "multiple-solution")
    return solved + multiple_solutions


def get_all_puzzles() -> List[List[List[int]]]:
    """
    Returns all available puzzle from every category; valid, unsolvable, unoffical
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
    Print the Sudoku grid in a readable format
    Show '.' for blank cells and adds lines to seperate subgrids
    """

    # Create 3 x 3 subgrids
    for i, row in enumerate(grid):
        # Draw a line every 3 rows to seperate subgrids
        if i > 0 and i % 3 == 0:
            print(" - - - + - - - + - - -")

        row_str = ""
        for j, val in enumerate(row):
            # Draw a vertical line every 3 columns to seperate subgrids
            if j > 0 and j % 3 == 0:
                row_str += " |"
            row_str += f" {val if val != 0 else '.'}"

        print(row_str)


def manual_input() -> list[list[int]]:
    """
    Prompt user to input a Sudoku puzzle line by line.
    Returns the constructed 9 x 9 grid.
    """

    print("Please enter your Sudoku puzzle line by line.")
    print("Use digits 1-9 for givens and 0 or . for blanks.")
    grid = []
    allowed_chars = set('123456789.')

    # Loops through each of the 9 lines while asking for a valid input
    for i in range(9):
        while True:
            line = input(f"Line {i + 1}: ").strip()

            #check the line has exaclty 9 character
            if len(line) != 9:
                print("Invalid input. Please enter exactly 9 characters")
                continue

            # Check all characters are valid
            invalid_found = False
            for c in line:
                if c not in allowed_chars:
                    invalid_found = True
                    break

            if invalid_found:
                print("Invalid input. Please enter only digits 1-9, 0 or . for blanks.")
                continue

            row = []
            for c in line:
                if c in '123456789':
                    row.append(int(c))
                else:
                    row.append(0)
            
            grid.append(row)
            break

    print_grid(grid)
    return grid

def print_status(is_consistent: bool, solved: bool) -> None:
    """
    Print a concise standardized status line:
    Arc-consistent: YES/NO | Solved: YES/NO"
    """

    if is_consistent:
        consistent_str = "YES"
    else:
        consistent_str = "NO"

    if solved:
        solved_str = "YES"
    else:
        solved_str = "NO"
    
    print(f"Arc-consistent: {consistent_str} | Solved: {solved_str}")