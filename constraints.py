"""
CP468 — constraints.py
Binary constraints and geometric relations for Sudoku.

Contributors:
    - (Name 1)
    - (Name 2)
    - (Name 3)
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
