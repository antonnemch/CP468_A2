"""
CP468 — backtracking.py
Additional algorithm when AC-3 does not finish: Backtracking search with optional
forward-checking and AC-3 as inference.

Contributors:
    - Jordan F.
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
    trail = Trail() #to keep track of variable assignments
    return _backtrack(csp, trail)


def _backtrack(csp: CSP, trail: Trail) -> bool:
    # if all variables are assigned and constraints are satisfied, move on
    if csp.is_solved():
        return True
    
    #Choose the next variable to assign using MRV
    var = heuristics.select_var_mrv(csp)

    
    if var is None:
        return False  # No unassigned variable found but puzzle not solved?

    # Get the values for the vairable, ordered by LCV
    values = heuristics.order_values_lcv(csp, var)


    for value in values:
        trail.push_frame() #Use the Trail to save the state before trying the value
        if _assign_and_infer(csp, var, value, trail):
            if _backtrack(csp, trail):
                return True    
        trail.pop_frame_and_undo(csp.domains) #If it doesnt work use the trail to undo the changes to try another value

    return False #No other value works, so backtrack


def _assign_and_infer(csp: CSP, var: Var, value: int, trail: Trail) -> bool:
    """
    Assign a value to a variable and run AC-3 inference.
    Returns False if inconsistency is detected anywhere.
    """

    # Record domain changes for var itself
    removed_vals = csp.domains[var] - {value}

    #Use trail to keep track of domain before we change it
    trail.record(var, removed_vals)

    # Assign the value
    csp.domains[var] = {value}

    # Forward checking
    for neighbor in csp.neighbors[var]:
        #If the value we assigned is in the neighbors domain, remove it
        if value in csp.domains[neighbor]:
            trail.record(neighbor, {value})
            csp.domains[neighbor].remove(value)
            #If it empties the neighbours domain, its a dead end
            if len(csp.domains[neighbor]) == 0:
                return False
            

    # Run AC-3 on neighbors of var for further inference
    arcs = []
    for neighbor in csp.neighbors[var]:
        arcs.append((neighbor, var))
    is_consistent, _ = ac3.ac3(csp, queue=arcs, track_queue=False)

    #Returns True ONLY if it still consistent after inference
    return is_consistent
