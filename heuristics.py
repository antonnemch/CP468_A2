"""
CP468 — heuristics.py
Heuristics for variable selection and value ordering to speed up backtracking.

Contributors:
    - (Name 1)
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

Functions to Implement:
    - def select_var_mrv(csp: CSP) -> Var
        # Minimum Remaining Values: pick an unassigned variable with the smallest domain (>1).

    - def degree_tiebreak(csp: CSP, candidates: list[Var]) -> Var
        # Among MRV ties, prefer the variable with the greatest number of unassigned neighbors.

    - def order_values_lcv(csp: CSP, var: Var) -> list[int]
        # Least Constraining Value: order values by how few options they eliminate for neighbors.

Notes:
    - "Unassigned" means domain size > 1.
    - These functions must NOT solve; they only rank choices.
"""
