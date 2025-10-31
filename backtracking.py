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
    """Efficient undo mechanism for domain changes"""

    def __init__(self):
        self.frames: List[List[tuple[Var, Set[int]]]] = []

    def push_frame(self):
        """Start new backtracking frame"""
        self.frames.append([])

    def record(self, var: Var, removed_values: Set[int]):
        """Record values removed from a variable's domain"""
        if removed_values and self.frames:
            self.frames[-1].append((var, removed_values.copy()))

    def pop_frame_and_undo(self, domains: Dict[Var, Set[int]]):
        """Undo all changes in the current frame"""
        if not self.frames:
            return
        frame = self.frames.pop()
        for var, removed_vals in reversed(frame):
            domains[var] |= removed_vals


def solve(csp: CSP) -> bool:
    """
    Solve CSP using backtracking with AC-3 inference
    """
    trail = Trail()
    return _backtrack(csp, trail)


def _backtrack(csp: CSP, trail: Trail) -> bool:
    if csp.is_solved():
        return True

    var = heuristics.select_var_mrv(csp)
    if var is None:
        return False  # No unassigned variable found but puzzle not solved?

    values = heuristics.order_values_lcv(csp, var)

    for value in values:
        trail.push_frame()
        if _assign_and_infer(csp, var, value, trail):
            if _backtrack(csp, trail):
                return True
        trail.pop_frame_and_undo(csp.domains)

    return False


def _assign_and_infer(csp: CSP, var: Var, value: int, trail: Trail) -> bool:
    """
    Assign a value to a variable and run AC-3 inference.
    Returns False if inconsistency is detected.
    """

    # Record domain changes for var itself
    removed_vals = csp.domains[var] - {value}
    trail.record(var, removed_vals)

    # Assign the value
    csp.domains[var] = {value}

    # Run AC-3 on neighbors of var
    arcs = [(neighbor, var) for neighbor in csp.neighbors[var]]
    is_consistent, _ = ac3.ac3(csp, queue=arcs, track_queue=False)

    return is_consistent
