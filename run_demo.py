"""
CP468 — run_demo.py
Demo & benchmarking harness for Sudoku-as-CSP.
Contributors:
    - Anton

Modes:
  - short  : run 1 example from each category; print AC-3 queue contents live
  - full   : run all available puzzles from all categories
  - manual : prompt for a puzzle; print AC-3 queue contents live

Outputs:
  - AC-3 queue trace (in short/manual)
  - Messages when switching from AC-3 to backtracking
  - Runtime per puzzle
  - Summary table with totals + file-by-file results
"""

from __future__ import annotations
import argparse
import time
from collections import deque
from typing import Iterable, List, Optional, Tuple
from pathlib import Path

import io_utils
from sudoku_csp import sudoku_csp_from_grid, CSP, Var
import ac3 as ac3_mod
import backtracking as bt


# ---------- Verbose AC-3 (local) ----------
def ac3_verbose(csp: CSP, queue: Optional[Iterable[Tuple[Var, Var]]] = None) -> Tuple[bool, int]:
    """AC-3 with live queue CONTENT printing."""
    arc_queue = deque(queue or csp.all_arcs())
    pops = 0

    def revise(Xi: Var, Xj: Var) -> bool:
        revised = False
        di = csp.domains[Xi]
        dj = csp.domains[Xj]
        to_remove = set()
        for x in di:
            if not any(csp.constraint(Xi, x, Xj, y) for y in dj):
                to_remove.add(x)
        if to_remove:
            di -= to_remove
            revised = True
        return revised

    step = 0
    while arc_queue:
        step += 1
        q_list = list(arc_queue)
        preview = ", ".join([f"{a}->{b}" for (a, b) in q_list[:12]])
        extra = "" if len(q_list) <= 12 else f" ... (+{len(q_list)-12} more)"
        print(f"[AC-3] Step {step:03d} | Queue size={len(q_list)} | {preview}{extra}")

        Xi, Xj = arc_queue.popleft()
        pops += 1

        if revise(Xi, Xj):
            if len(csp.domains[Xi]) == 0:
                print("[AC-3] Domain wipe-out -> inconsistent")
                return False, pops
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    arc_queue.append((Xk, Xi))
    return True, pops


# ---------- Helper: run one puzzle ----------

def run_one_puzzle(grid: List[List[int]], *, verbose_queue: bool, label: str) -> dict:
    """
    Run AC-3 (verbose or standard), then backtracking if needed.
    Returns a metrics dict.
    """
    metrics = {
        "label": label,              # >>> added
        "ac3_used": True,
        "ac3_pops": 0,
        "ac3_consistent": False,
        "bt_used": False,
        "solved": False,
        "time_sec": 0.0,
        "result_str": "",            # >>> added
    }

    print(f"\n=== Running: {label} ===")
    io_utils.print_grid(grid)

    t0 = time.perf_counter()
    if verbose_queue:
        print("\n[run] Starting AC-3 (verbose)...")
        consistent, pops = ac3_verbose(sudoku_csp_from_grid(grid))
        q_lengths = None
    else:
        print("\n[run] Starting AC-3...")
        csp = sudoku_csp_from_grid(grid)
        consistent, q_lengths = ac3_mod.ac3(csp, track_queue=True)
        pops = len(q_lengths) if q_lengths is not None else 0

    metrics["ac3_consistent"] = bool(consistent)
    metrics["ac3_pops"] = int(pops)

    if not consistent:
        metrics["time_sec"] = time.perf_counter() - t0
        metrics["result_str"] = "UNSOLVABLE"
        io_utils.print_status(is_consistent=False, solved=False)
        print(f"[run] Finished (AC-3 inconsistent). time={metrics['time_sec']:.4f}s")
        return metrics

    csp = sudoku_csp_from_grid(grid)
    ac3_mod.ac3(csp)
    if csp.is_solved():
        metrics["solved"] = True
        metrics["time_sec"] = time.perf_counter() - t0
        metrics["result_str"] = "SOLVED BY AC-3"
        io_utils.print_status(is_consistent=True, solved=True)
        print("\nSolution:")
        io_utils.print_grid(csp.to_grid())
        print(f"[run] Finished (solved by AC-3). time={metrics['time_sec']:.4f}s")
        return metrics

    print("[run] AC-3 did not finish → switching to Backtracking...")
    metrics["bt_used"] = True

    csp = sudoku_csp_from_grid(grid)
    consistent, _ = ac3_mod.ac3(csp)
    solved = bt.solve(csp)
    metrics["solved"] = bool(solved)
    metrics["time_sec"] = time.perf_counter() - t0
    metrics["result_str"] = "SOLVED BY BACKTRACKING" if solved else "NO SOLUTION"

    io_utils.print_status(is_consistent=True, solved=metrics["solved"])
    if solved:
        print("\nSolution:")
        io_utils.print_grid(csp.to_grid())
    print(f"[run] Finished. time={metrics['time_sec']:.4f}s")

    return metrics


# ---------- Summary printer ----------

def print_summary(results: List[dict]) -> None:
    print("\n==================== SUMMARY ====================")
    total = len(results)
    total_time = sum(r["time_sec"] for r in results)
    avg_time = total_time / total if total else 0.0

    solved = sum(1 for r in results if r["solved"])
    by_ac3 = sum(1 for r in results if "AC-3" in r["result_str"])
    by_bt = sum(1 for r in results if "BACKTRACKING" in r["result_str"])
    unsat = sum(1 for r in results if r["result_str"] == "UNSOLVABLE")

    print(f"Total puzzles run     : {total}")
    print(f"Solved (total)        : {solved}")
    print(f"  - by AC-3 only      : {by_ac3}")
    print(f"  - by Backtracking   : {by_bt}")
    print(f"Unsolvable (AC-3)     : {unsat}")
    print(f"Total runtime (s)     : {total_time:.4f}")
    print(f"Average runtime (s)   : {avg_time:.4f}")
    print("-------------------------------------------------")
    print("Per-file results:")
    for r in results:                      # >>> added
        print(f"  {r['label']:<35} : {r['result_str']:<22} | {r['time_sec']:.4f} s")
    print("=================================================")


# ---------- Runner modes ----------

def run_short():
    print("\n=== SHORT TEST MODE ===")
    batches = [
        ("valid", io_utils.get_valid_puzzles()),
        ("unsolvable", io_utils.get_unsolvable_puzzles()),
        ("unofficial", io_utils.get_unofficial_puzzles()),
    ]
    results = []
    for label, puzzles in batches:
        if not puzzles:
            print(f"[info] No puzzles in {label}/")
            continue
        grid = puzzles[0]
        file_label = f"{label}/example_1"
        results.append(run_one_puzzle(grid, verbose_queue=True, label=file_label))
    print_summary(results)


def run_full():
    print("\n=== FULL TEST MODE ===")
    results = []
    all_puzzles = (
        list((p, "valid") for p in io_utils.get_valid_puzzles())
        + list((p, "unsolvable") for p in io_utils.get_unsolvable_puzzles())
        + list((p, "unofficial") for p in io_utils.get_unofficial_puzzles())
    )
    for i, (grid, cat) in enumerate(all_puzzles, 1):
        label = f"{cat}/puzzle_{i}"
        results.append(run_one_puzzle(grid, verbose_queue=False, label=label))
    print_summary(results)


def run_manual():
    print("\n=== MANUAL MODE ===")
    grid = io_utils.manual_input()
    results = [run_one_puzzle(grid, verbose_queue=True, label="manual_input")]
    print_summary(results)


# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(description="CP468 Sudoku CSP Demo Runner")
    parser.add_argument("--mode", choices=["short", "full", "manual"], default="short")
    args = parser.parse_args()

    if args.mode == "short":
        run_short()
    elif args.mode == "full":
        run_full()
    elif args.mode == "manual":
        run_manual()


if __name__ == "__main__":
    main()
