"""
CP468 — constraints.py
Binary constraints and geometric relations for Sudoku.

Contributors:
    - Roop - Code
    - Anton - documentation
    - Julian 
    - (Name 4)
    - (Name 5)

Functions to Implement:
    - def binary_neq(Xi: Var, a: int, Xj: Var, b: int) -> bool
        # Returns True iff a != b (Sudoku's pairwise inequality).

    - def same_row(a: Var, b: Var) -> bool
        # True if a and b share the same row.

    - def same_col(a: Var, b: Var) -> bool
        # True if a and b share the same column.

    - def same_box(a: Var, b: Var) -> bool
        # True if a and b share the same 3x3 subgrid (rows//3, cols//3 equal).

Notes:
    - Var is a tuple[int,int] with 0-based indexing.
    - These helpers are used by sudoku_csp.sudoku_csp_from_grid to build neighbors.
"""
from typing import Tuple

Var = Tuple[int, int]  # (row, col), 0..8

def binary_neq(x1: Var, a: int, x2: Var, b: int) -> bool:
    return a != b

def same_row(x1: Var, x2: Var) -> bool:
    return x1[0] == x2[0]

def same_col(x1: Var, x2: Var) -> bool:
    return x1[1] == x2[1]

def same_box(x1: Var, x2: Var) -> bool:
    return (x1[0] // 3 == x2[0] // 3) and (x1[1] // 3 == x2[1] // 3)
