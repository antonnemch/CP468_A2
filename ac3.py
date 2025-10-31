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
