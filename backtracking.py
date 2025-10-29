"""
CP468 — backtracking.py
Additional algorithm when AC-3 does not finish: Backtracking search with optional
forward-checking and/or AC-3 as inference.

Contributors:
    - (Name 1)
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

Functions / Objects to Implement:
    - def solve(csp: CSP) -> bool
        Behavior:
            - Returns True if a complete assignment (singleton domains) is found.
            - Mutates csp.domains in place to reflect the solution.
            - Strategy:
                1) Select an unassigned variable (domain size > 1). (heuristics.select_var_mrv)
                2) Order its values. (heuristics.order_values_lcv)
                3) Try a value:
                    - Temporarily assign (reduce domain to {v}).
                    - Inference: forward-checking and/or run AC-3 on affected arcs.
                    - Recurse; on failure, undo changes (Trail).
                4) If none work, return False.

    - class Trail:
        Purpose:
            - Record domain prunes and assignments to allow efficient undo on backtrack.
        Methods:
            - push_frame()
            - record(var: Var, removed_values: set[int])
            - pop_frame_and_undo(domains: dict[Var, set[int]])

Hooks (import from heuristics.py):
    - heuristics.select_var_mrv(csp: CSP) -> Var
    - heuristics.degree_tiebreak(csp: CSP, candidates: list[Var]) -> Var
    - heuristics.order_values_lcv(csp: CSP, var: Var) -> list[int]

Contracts:
    - Must preserve CSP invariants.
    - Should avoid deep-copying full domains at each node; use Trail for efficiency.
"""
