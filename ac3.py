"""
CP468 — ac3.py
AC-3 algorithm for enforcing arc consistency on a CSP.

Contributors:
    - Jordan F.
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

Functions:
    - ac3(csp, queue, track_queue) -> (bool, list[int] | None)
    - revise(csp, Xi, Xj) -> bool
"""

from collections import deque
from typing import Iterable, Optional
from sudoku_csp import CSP, Var

def ac3(csp: CSP, queue: Optional[Iterable[tuple[Var, Var]]] = None, track_queue: bool = False) -> tuple[bool, Optional[list[int]]]:
    """
    Enforce arc consistency using AC3 algorithm
    Args:
        csp: The constraint satisfaction problem
        queue: Initial arcs to process (defaults to all arcs)
        track_queue: Whether to track queue length at each step
    Returns:
        is_consistent: True if arc-consistent, false if inconsistency detected --> backtracking
        queue_lengths: List of queue sizes at each pop (only if track_queue=True)
    """
    
    if queue is None:
        arc_queue = deque(csp.all_arcs())
    else:
        arc_queue = deque(queue)
    queue_lengths = [] if track_queue else None
    
    while arc_queue:
        if track_queue:
            queue_lengths.append(len(arc_queue))
        Xi, Xj = arc_queue.popleft()
        
        if revise(csp, Xi, Xj):
            if len(csp.domains[Xi]) == 0:
                return False,queue_lengths
            
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    arc_queue.append((Xk, Xi))
    
    return True,queue_lengths

def revise(csp: CSP, Xi: Var, Xj: Var) -> bool:
    """
    Make Xi arc consistent w.r.t. Xj.
    Args:
        csp: The constraint satisfaction problem
        Xi: Source var
        Xj: Target var
    Returns:
        True if domain of Xi was revised (vals removed), false otherwise
    """
    
