"""
CP468 — sudoku_csp.py
CSP definition and Sudoku-specific builder.

Contributors:
    - Julian Rincon - code
    - Anton - documentation
    - Jordan F. - fix neighbor construction
"""

from __future__ import annotations
from typing import Callable, Dict, Iterable, List, Set, Tuple
import constraints

Var = Tuple[int, int]  # (row, col), 0-based
Value = int            # 1..9


def _binary_neq_adapter(x1: Var, a: Value, x2: Var, b: Value) -> bool:
    """Adapter for the binary_neq constraint"""
    return constraints.binary_neq(x1, x2, a, b)


def _same_box_correct(x1: Var, x2: Var) -> bool:
    """Return True if x1 and x2 are in the same 3x3 box"""
    return (x1[0] // 3 == x2[0] // 3) and (x1[1] // 3 == x2[1] // 3)


class CSP:
    """CSP object for Sudoku"""

    def __init__(
        self,
        variables: List[Var],
        domains: Dict[Var, Set[Value]],
        neighbors: Dict[Var, Set[Var]],
        constraint: Callable[[Var, Value, Var, Value], bool],
    ) -> None:
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint = constraint

    def all_arcs(self) -> Iterable[Tuple[Var, Var]]:
        for xi in self.variables:
            for xj in self.neighbors.get(xi, ()):
                yield (xi, xj)

    def is_solved(self) -> bool:
        for v in self.variables:
            if len(self.domains.get(v, ())) != 1:
                return False
        for xi in self.variables:
            vi = next(iter(self.domains[xi]))
            for xj in self.neighbors.get(xi, ()):
                if xi < xj:
                    vj = next(iter(self.domains[xj]))
                    if not self.constraint(xi, vi, xj, vj):
                        return False
        return True

    def to_grid(self) -> List[List[int]]:
        """Return a 9x9 grid of ints; 0 for unsolved cells"""
        grid: List[List[int]] = [[0 for _ in range(9)] for _ in range(9)]
        for (r, c) in self.variables:
            d = self.domains.get((r, c), set())
            grid[r][c] = next(iter(d)) if len(d) == 1 else 0
        return grid

    def __repr__(self) -> str:
        assigned = sum(1 for v in self.variables if len(self.domains[v]) == 1)
        return (
            f"CSP(vars={len(self.variables)}, "
            f"assigned={assigned}, "
            f"arcs={sum(len(self.neighbors[v]) for v in self.variables)})"
        )


def sudoku_csp_from_grid(grid: List[List[int]]) -> CSP:
    """Construct a Sudoku CSP from a 9x9 integer grid (0=empty)"""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("Grid must be 9x9.")
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if not isinstance(v, int) or not (0 <= v <= 9):
                raise ValueError("Grid values must be integers in 0..9.")

    variables: List[Var] = [(r, c) for r in range(9) for c in range(9)]
    full_domain: Set[Value] = set(range(1, 10))

    # Initialize domains
    domains: Dict[Var, Set[Value]] = {}
    for (r, c) in variables:
        val = grid[r][c]
        domains[(r, c)] = {val} if 1 <= val <= 9 else set(full_domain)

    # Build neighbors (row, column, box)
    neighbors: Dict[Var, Set[Var]] = {v: set() for v in variables}
    for (r1, c1) in variables:
        for (r2, c2) in variables:
            if (r1, c1) == (r2, c2):
                continue
            if r1 == r2 or c1 == c2 or _same_box_correct((r1, c1), (r2, c2)):
                neighbors[(r1, c1)].add((r2, c2))

    return CSP(
        variables=variables,
        domains=domains,
        neighbors=neighbors,
        constraint=_binary_neq_adapter,
    )
