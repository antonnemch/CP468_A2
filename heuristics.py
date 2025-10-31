"""
CP468 — heuristics.py
Variable selection and value ordering heuristics for backtracking.

Contributors:
    - Jordan F.

Functions:
    - select_var_mrv(csp) -> Var
    - degree_tiebreak(csp, candidates) -> Var
    - order_values_lcv(csp, var) -> list[int]
"""

from typing import List, Optional
from sudoku_csp import CSP, Var

def select_var_mrv(csp: CSP) -> Optional[Var]:
    """
    Minimum Remaining values heuristic with degree tiebreaker
    Returns unassigned variable with smallest domain and ties are 
     broken by degree heuristic (highest # of constraints on unassigned neighbors).
    """
    
    unassigned = [v for v in csp.variables if len(csp.domains[v]) > 1]
    if not unassigned:
        return None
    
    min_size = min(len(csp.domains[v]) for v in unassigned)
    candidates = [v for v in unassigned if len(csp.domains[v]) == min_size]
    
    if len(candidates) == 1:
        return candidates[0]
    
    return degree_tiebreak(csp, candidates)
