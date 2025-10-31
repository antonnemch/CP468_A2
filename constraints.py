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

def binary_neq(x1, x2, a, b):
    """Sudoku inequality constraint"""
    return a != b

def same_row(x1, x2):
    return x1[0] == x2[0]

def same_col(x1, x2):
    return x1[1] == x2[1]

def same_box(x1, x2):
    """Return True if x1 and x2 share the same 3x3 subgrid"""
    return (x1[0] // 3 == x2[0] // 3) and (x1[1] // 3 == x2[1] // 3)
