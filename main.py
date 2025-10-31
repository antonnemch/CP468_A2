"""
CP468 — main.py
Entry point and orchestration for Sudoku-as-CSP.
Contributors:
    - Anton
    - Jordan F.
    - (Name 3)
    - (Name 4)
    - (Name 5)
    
"""

import argparse
import sys
from io_utils import read_puzzle, print_grid, print_status
from sudoku_csp import sudoku_csp_from_grid
import ac3
import backtracking
  

def solve_puzzle(puzzle_path: str, track_queue: bool = False, show_queue: bool = False):
    """
    Main solver: read puzzle → AC-3 → backtracking (if AC-3 can't solve)
    """
    print(f"\n\nSolving {puzzle_path}\n\n")

    p = read_puzzle(puzzle_path)
    print("Initial puzzle:")
    print_grid(p)
    
    csp = sudoku_csp_from_grid(p)
    is_consistent, queue_lengths = ac3.ac3(csp,track_queue=track_queue)
    
    if show_queue and queue_lengths:
        print(f"\nAC-3 queue lengths: {queue_lengths}")
        print(f"Total AC-3 iterations: {len(queue_lengths)}")
    
    if not is_consistent:
        print("\nPuzzle is unsolvable (AC3 detected inconsistency)")
        print_status(is_consistent=False, solved=False)
        return
    
    solved = csp.is_solved()
    
    if solved:
        print("\nPuzzle solved by AC-3!\n")
        print_status(is_consistent=True, solved=True)
        print("Solution:")
        print_grid(csp.to_grid())
        return
    
    print("\nAC-3 was not able to solve, running backtracking search")
    
    if backtracking.solve(csp):
        print("\nPuzzle solved by backtracking!\n")
        print_status(is_consistent=True, solved=True)
        print("\nSolution:")
        print_grid(csp.to_grid())
    else:
        print("\nNo solution found")
        print_status(is_consistent=True, solved=False)

def main():
    parser.add_argument("puzzle_path")
    parser.add_argument("--track-queue", action="store_true")
    parser.add_argument("--show-queue", action="store_true")
    args = parser.parse_args()
    
    try:
        solve_puzzle(args.puzzle_path, args.track_queue, args.show_queue)
    except FileNotFoundError:
        print(f"File not found: {args.puzzle_path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No arguments provided, running demo mode")
        print("For solver mode use: python main.py <puzzle_path> [--track-queue] [--show-queue]")
        print("\nExample: python main.py test_puzzles/valid/puzzle1.txt --track-queue --show-queue")
        #demo_io()
    else:
        main()
