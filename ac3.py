"""
CP468 — ac3.py
AC-3 algorithm for enforcing arc consistency on a CSP.

Contributors:
    - Jordan F.
"""

from collections import deque
from typing import Iterable, Optional
from sudoku_csp import CSP, Var

def ac3(csp: CSP, queue: Optional[Iterable[tuple[Var, Var]]] = None, track_queue: bool = False) -> tuple[bool, Optional[list[int]]]:
    """
    AC-3 Algorithm to ensure arc consistency
    
    Inputs:
        constraint satifaction problem
        initial arcs to process in a queue (can be none)
        a queue_tracker if needed
    
    Returns whether its arc consistent and the optional queue length
    """
    
    # If no initial queue is given, get all arcs from the CSP
    if queue is None:
        arc_queue = deque(csp.all_arcs())
    else:
        arc_queue = deque(queue)
    
    # Only track queue size of needed
    if track_queue:
        queue_lengths = []
    else:
        queue_lengths = None


    while arc_queue:
        # If we are tracking the queue size, record the current length
        if track_queue and queue_lengths is not None:
            queue_lengths.append(len(arc_queue))
            
        # Take the next arc off the queue
        Xi, Xj = arc_queue.popleft()
        
        # Check the domain of Xi based on Xj
        if revise(csp, Xi, Xj):
            #If the domain of Xi is empty then the CSP is inconsistent
            if len(csp.domains[Xi]) == 0:
                return False,queue_lengths
            
            # Add all arcs (Xk, Xi) back to the queue for neighbors Xk of Xi, excluding Xj
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    arc_queue.append((Xk, Xi))
    
    # Returns true if no conficlts are found
    return True,queue_lengths

def revise(csp: CSP, Xi: Var, Xj: Var) -> bool:
    """
    Make Xi arc consistent w.r.t. Xj.
    Args:
        csp: The constraint satisfaction problem
        Xi: Source var
        Xj: Target var
    Returns:
        True if value is removed, false otherwise
    """

    
    revised = False
    domain_Xi = csp.domains[Xi]
    domain_Xj = csp.domains[Xj]

    #store values from the domain of Xi that should be removed
    remove = set()
    
    for x in domain_Xi:
        satisfied = False #Only true if x has a valid partner in the domain of Xj
        for k in domain_Xj:
            if csp.constraint(Xi, x,Xj, k):
                satisfied = True
                break
        
        #If no value in Xj satisfies the constraint, x will be removed
        if not satisfied:
            remove.add(x)
            revised = True
    #Remove the values from the domain of Xi that didnt work
    domain_Xi -= remove
    
    return revised


    
