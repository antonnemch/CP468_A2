# CP468 – Sudoku CSP Test Suite

This folder contains the complete set of Sudoku puzzles used to test the **AC-3 constraint-based solver** and optional **backtracking** extension.  
The collection was assembled from well-known public sources and a few simple handmade examples to ensure coverage across all edge and complexity cases.

---

## 📁 Folder Overview

### `valid/`
Contains **properly constructed, solvable Sudokus** with unique solutions.
- **Purpose:** Baseline functional correctness — verifying that AC-3 achieves arc-consistency without error and that backtracking converges to the unique valid grid.
- **Content:** Includes easy, intermediate, and difficult puzzles (several from *Sandiway Fong’s Sudoku Examples* and *Sudopedia Valid Test Cases*).
- **Expected outcome:** AC-3 alone may partially solve; final solver must reach full solution.

### `unsolvable/`
Contains **invalid or contradictory Sudokus** that cannot be satisfied.
- **Purpose:** Robustness testing — detecting inconsistent initial assignments and domain wipe-outs.
- **Content:** Drawn primarily from *Sudopedia Invalid Test Cases* and custom examples (duplicate digits in row, column, or box).
- **Expected outcome:** AC-3 must report inconsistency (domain empty), solver terminates gracefully.

### `multiple_solutions/`
Contains **under-constrained puzzles** that have more than one valid solution.
- **Purpose:** Verifies solver stability when arc-consistency alone cannot guarantee uniqueness.
- **Content:** Adapted from *Sudopedia Valid Test Cases* “multiple-solution” section and similar open examples.
- **Expected outcome:** AC-3 leaves multiple values per cell; backtracking should find one valid grid but not claim uniqueness.

### `solved/`
Contains **fully solved grids/single hole grids** used for regression and I/O validation.
- **Purpose:** Ensures that already-complete puzzles are detected as solved without modification.
- **Expected outcome:** AC-3 runs trivially consistent; solver reports “Arc-consistent: YES | Solved: YES”.

---

## 🔍 Test Philosophy

This dataset was curated to exercise every important code path in a Sudoku-as-CSP solver:

| Category | Tests | What It Verifies |
|-----------|--------|------------------|
| **Empty / sparse** | `empty1.txt`, `empty2.txt` | Initial domain setup and AC-3 propagation correctness |
| **Single-hole** | `last_empty_square.txt` | Simple logical deductions via constraint propagation |
| **Contradictory givens** | `duplicate_row.txt`, `duplicate_box.txt`, etc. | Proper detection of unsatisfiable constraints |
| **Hard valid puzzles** | `HardestSudokusThread-*.txt` | Interaction between AC-3 pruning and backtracking heuristics |
| **Multiple / Unofficial** | `four_solutions.txt`, etc. | Non-unique but valid grids; solver must still produce one |
| **Solved** | `solved1.txt`, `solved2.txt` | Solver output stability and idempotence |

---

## 🧩 Sources and References

- *Sudopedia — Invalid Test Cases*  
  <http://sudopedia.enjoysudoku.com/Invalid_Test_Cases.html>  
  (Used for unsolvable and duplicate-constraint examples.)

- *Sudopedia — Valid Test Cases*  
  <https://www.sudopedia.org/wiki/Valid_Test_Cases>  
  (Used for multiple-solution and standard valid examples.)

- *Sandiway Fong, University of Arizona — Sudoku Examples*  
  <https://sandiway.arizona.edu/sudoku/examples.html>  
  (Used for easy, intermediate, and hard valid puzzles.)

- *Enjoy Sudoku Forum — “The Hardest Sudokus” thread*  
  <http://forum.enjoysudoku.com/the-hardest-sudokus-new-thread-t6539.html>  
  (Used for extremely difficult benchmark puzzles such as the *AI Escargot* class.)

- *Handmade examples*  
  A few simple grids (e.g., trivial and single-hole puzzles) created manually to test specific code paths and domain setup.

---

### ✅ Summary

Together, these subfolders provide:
- Broad **difficulty coverage** (empty → AI-hard).  
- Clear **failure modes** for AC-3 domain wipe-outs.  
- Examples that **separate arc-consistency from full satisfaction**.  
- Reproducible, source-linked provenance for grading and demos.

