"""
CP468 — io_utils.py
Reading and writing Sudoku puzzles.

Contributors:
    - (Name 1)
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

Functions to Implement:
    - def read_puzzle(path: str) -> list[list[int]]
        Format:
            - 9 lines × 9 characters.
            - '1'..'9' for givens.
            - '0' or '.' for blanks.
        Output:
            - 9×9 list of ints (0 for blank).
        Validation:
            - Assert 9 rows; each row has 9 valid characters.

    - def write_grid(path: str, grid: list[list[int]]) -> None
        Behavior:
            - Writes 9 lines of 9 digits.
            - Uses '0' for unknowns.
"""
