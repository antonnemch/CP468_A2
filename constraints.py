"""
CP468 — constraints.py
Binary constraints and geometric relations for Sudoku.

Contributors:
    - Roop - code
    - Anton - documentation
    - (Name 3)
    - (Name 4)
    - (Name 5)

Functions to Implement:
    - def binary_neq(x1: Var, a: int, x2: Var, b: int) -> bool
        # Returns True iff a != b (Sudoku's pairwise inequality).

    - def same_row(x1: Var, x2: Var) -> bool
        # True if x1 and x2 share the same row.

    - def same_col(x1: Var, x2: Var) -> bool
        # True if x1 and x2 share the same column.

    - def same_box(x1: Var, x2: Var) -> bool
        # True if x1 and x2 share the same 3x3 subgrid (rows//3, cols//3 equal).

Notes:
    - Var is a tuple[int,int] with 0-based indexing.
    - These helpers are used by sudoku_csp.sudoku_csp_from_grid to build neighbors.
"""

def binary_neq(x1, a, x2, b):
    return a != b

def same_row(x1, x2):
    return x1[0] == x2[0]

def same_col(x1, x2):
    return x1[1] == x2[1]

def same_box(x1, x2):
    r1, c1 = x1
    r2, c2 = x2
    return (r1 // 3 == r2 // 3) and (c1 // 3 == c2 // 3)

