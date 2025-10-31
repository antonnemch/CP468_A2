"""
CP468 — constraints.py
Binary constraints and geometric relations for Sudoku.

Contributors:
    - Jordan F. (fixed)
    - Roop (original)
    - Anton (documentation)
"""

from typing import Tuple

Var = Tuple[int, int]  # (row, col), 0-based

def binary_neq(x1: Var, x2: Var, a: int, b: int) -> bool:
    """
    Binary inequality constraint.
    Returns True if values a and b are different.
    """
    return a != b

def same_row(x1: Var, x2: Var) -> bool:
    """
    True if two variables are in the same row.
    """
    return x1[0] == x2[0]

def same_col(x1: Var, x2: Var) -> bool:
    """
    True if two variables are in the same column.
    """
    return x1[1] == x2[1]

def same_box(x1: Var, x2: Var) -> bool:
    """
    True if two variables are in the same 3x3 subgrid.
    Uses integer division for 0-based indices.
    """
    return (x1[0] // 3 == x2[0] // 3) and (x1[1] // 3 == x2[1] // 3)
