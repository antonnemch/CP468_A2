"""
CP468 — sudoku_csp.py
CSP definition and Sudoku-specific builder.

Contributors:
    - (Name 1)
    - (Name 2)
    - (Name 3)
    - (Name 4)
    - (Name 5)

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
