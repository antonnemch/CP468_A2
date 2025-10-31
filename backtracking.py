"""
CP468 — backtracking.py
Additional algorithm when AC-3 does not finish: Backtracking search with optional
forward-checking and/or AC-3 as inference.

Contributors:
    - Jordan F.
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

Classes:
    - Trail: Efficient undo mechanism for domain changes
    
Functions:
    - solve(csp) -> bool
"""

from typing import Dict, List, Set
from sudoku_csp import CSP, Var
import heuristics
import ac3

class Trail:
    """Documents domain changes for efficient backtracking algorithm"""
    
    def __init__(self):
        self.frames: List[List[tuple[Var,Set[int]]]] = []
