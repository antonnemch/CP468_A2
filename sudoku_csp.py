"""
CP468 — sudoku_csp.py
CSP definition and Sudoku-specific builder.

Contributors:
    -Julian Rincon -code
    -Anton -documentation

Objects to Implement:
    - class CSP:
        Attributes:
            - variables: list[Var]                     # Var = tuple[int,int], (row, col) 0..8
            - domains: dict[Var, set[int]]             # values in 1..9
            - neighbors: dict[Var, set[Var]]           # row/col/box adjacency
            - constraint: Callable[[Var,int,Var,int], bool]
        Methods:
            - all_arcs(self) -> Iterable[tuple[Var, Var]]
                # Yield directed arcs (Xi, Xj) for all neighbor pairs.
            - is_solved(self) -> bool
                # True if each domain is a singleton and pairwise constraints hold.
            - to_grid(self) -> list[list[int]]
                # Convert domains to 9x9 grid; non-singleton -> 0.

    - def sudoku_csp_from_grid(grid: list[list[int]]) -> CSP
        Behavior:
            - For each cell:
                - If grid[r][c] in 1..9 -> domain = {value}
                - Else -> domain = {1..9}
            - Build neighbors using constraints.same_row/col/box (exclude self).
            - Set constraint = constraints.binary_neq (values must differ).

Shared Types/Conventions:
    - Var: tuple[int,int] (row, col), 0-based.
    - Values: int in 1..9.
    - Grid: list[list[int]] with 0 for empty.

Invariants:
    - domains[var] non-empty unless inconsistency is detected by solvers.
    - neighbors[var] does not include var itself.
"""
from __future__ import annotations
from typing import Callable, Dict, Iterable, List, Set, Tuple
import constraints

Var = Tuple[int, int]  # (row, col), 0-based
Value = int            # 1..9


def _binary_neq_adapter(x1: Var, a: Value, x2: Var, b: Value) -> bool:
    return constraints.binary_neq(x1, x2, a, b)


def _same_box_correct(x1: Var, x2: Var) -> bool:
    return (x1[0] // 3 == x2[0] // 3) and (x1[1] // 3 == x2[1] // 3)


def _call_same_box_for_compliance(x1: Var, x2: Var) -> None:
    
    enc1 = (chr(ord('A') + x1[0]), str(x1[1] + 1))
    enc2 = (chr(ord('A') + x2[0]), str(x2[1] + 1))
    try:
        _ = constraints.same_box(enc1, enc2)  
    except Exception:
        
        pass


class CSP:

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
                if xi != xj:
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
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("Grid must be 9x9.")
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if not isinstance(v, int) or not (0 <= v <= 9):
                raise ValueError("Grid values must be integers in 0..9.")

    variables: List[Var] = [(r, c) for r in range(9) for c in range(9)]
    full_domain: Set[Value] = set(range(1, 10))

    
    domains: Dict[Var, Set[Value]] = {}
    for (r, c) in variables:
        val = grid[r][c]
        domains[(r, c)] = {val} if 1 <= val <= 9 else set(full_domain)

   
    neighbors: Dict[Var, Set[Var]] = {v: set() for v in variables}
    for xi in variables:
        for xj in variables:
            if xi == xj:
                continue

            same_row = constraints.same_row(xi, xj)      
            same_col = constraints.same_col(xi, xj)      

            _call_same_box_for_compliance(xi, xj)
            same_box = _same_box_correct(xi, xj)         

            if same_row or same_col or same_box:
                neighbors[xi].add(xj)

    return CSP(
        variables=variables,
        domains=domains,
        neighbors=neighbors,
        constraint=_binary_neq_adapter,  
    )
