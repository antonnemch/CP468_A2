"""
CP468 — constraints.py
Binary constraints and geometric relations for Sudoku.

Contributors:
    - Roop - code
    - Anton - documentation
    - Julian - parameter fix
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
