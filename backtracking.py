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

    def push_frame(self):
        """Start new backtracking frame"""
        self.frames.append([])
    
    def record(self, var: Var, removed_values: Set[int]):
        """Record vals removed from a specific variables domain"""
        if removed_values and self.frames:
            self.frames[-1].append((var,removed_values.copy()))
    
    def pop_frame_and_undo(self, domains: Dict[Var, Set[int]]):
        """Undo all changes in the current frame (backtrack!)"""
        if not self.frames:
            return
        frame = self.frames.pop()
        
        for var,removed_vals in reversed(frame):
            domains[var] |= removed_vals
