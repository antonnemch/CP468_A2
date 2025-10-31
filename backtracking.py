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


def solve(csp: CSP) -> bool:
    """
    Solve CSP Sudoku puzzle using backtracking algorithm
    
    Argumentss:
        csp: The constraint satisfaction problem to solve
    Returns:
        True if solution found, false otherwise
    """
    trail = Trail()
    return _backtrack(csp, trail)


def _backtrack(csp: CSP, trail:Trail) -> bool:
    """Recursive backtracking helper func"""
    
    if csp.is_solved():
        return True
    
    var = heuristics.select_var_mrv(csp)
    if var is None:
        return True
    values = heuristics.order_values_lcv(csp, var)
    
    for value in values:
        trail.push_frame()
        if _assign_and_infer(csp,var, value, trail):
            if _backtrack(csp, trail):
                return True
        
        trail.pop_frame_and_undo(csp.domains)
    
    return False


def _assign_and_infer(csp: CSP, var: Var, value: int, trail: Trail) -> bool:
    """
    Assign a value to variable then run AC-3 inference,
    returns False if inconsistency
    """
    
    saved_domains = {}
    for v in csp.variables:
        saved_domains[v] = csp.domains[v].copy()
    
    domain = csp.domains[var]
    domain.clear()
    domain.add(value)
    
    arcs = [(xj,var) for xj in csp.neighbors[var]]
    is_consistent, _ = ac3.ac3(csp, queue=arcs, track_queue=False)
    
    if not is_consistent:
        return False
    
    for v in csp.variables:
        
        removed = saved_domains[v] - csp.domains[v]
        
        if removed:
            trail.record(v, removed)
            
    return True
