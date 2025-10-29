"""
CP468 — ac3.py
AC-3 algorithm for enforcing arc consistency on a CSP.

Contributors:
    - (Name 1)
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

Functions to Implement:
    - def ac3(csp: CSP, queue: Iterable[tuple[Var,Var]] | None = None,
              track_queue: bool = False) -> tuple[bool, list[int] | None]
        Behavior:
            - Initialize a queue with provided arcs or csp.all_arcs().
            - Pop arcs; call revise(csp, Xi, Xj).
            - If domain of Xi becomes empty -> return (False, queue_lengths?).
            - If revise prunes Xi, enqueue (Xk, Xi) for all Xk in neighbors[Xi] \ {Xj}.
            - If track_queue, collect the queue length at each pop and return it.

    - def revise(csp: CSP, Xi: Var, Xj: Var) -> bool
        Behavior:
            - For each x in domain(Xi), keep it iff there exists y in domain(Xj)
              such that csp.constraint(Xi, x, Xj, y) is True.
            - Remove unsupported x; return True if any were removed.

Contracts:
    - Uses only the CSP interface (domains, neighbors, constraint, all_arcs()).
    - Does NOT assume Sudoku-specific logic.
    - Returns a boolean for arc-consistency and optional queue trace.

Performance Notes:
    - Prefer sets for domains.
    - Use deque for the queue (if implementing now).
"""
