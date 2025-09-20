#!/usr/bin/env python3
"""
demo_run_parser.py

An original demo script that shows how the AI Agent project works and
demonstrates a generated parser (ICICI by default). This is safe to include
in your repo — it performs the same user-visible functionality as the
example you provided but is written from scratch.

Features:
- Prints a short architecture overview
- Shows expected project layout
- Dynamically imports and runs a parser from custom_parsers/<bank>_parser.py
- Compares parser output to the expected CSV and prints a summary
- Friendly messages and error handling
"""

import os
import sys
import argparse
import importlib
from pathlib import Path

import pandas as pd


def show_architecture():
    print("AI Agent — Bank Statement Parser")
    print("=" * 56)
    print("High-level flow:")
    print("  Planner  ->  Code generator  ->  Code tester  ->  (Success / Self-correct)")
    print("  (Up to 3 attempts to self-correct generated parsers)\n")


def show_project_layout():
    print("Expected project layout (important files/folders):")
    print("  <repo-root>/")
    print("    agent.py")
    print("    custom_parsers/")
    print("      └── <bank>_parser.py      # generated or hand-written parser")
    print("    data/")
    print("      └── <bank>/")
    print("          ├── <bank>_sample.pdf")
    print("          └── <bank>_sample.csv")
    print("    tests/")
    print("    README.md\n")


def make_paths(bank: str):
    root = Path.cwd()
    data_dir = root / "data" / bank
    pdf_path = data_dir / f"{bank}_sample.pdf"
    csv_path = data_dir / f"{bank}_sample.csv"
    return pdf_path, csv_path


def import_parser(bank: str):
    """
    Dynamically import custom_parsers.<bank>_parser and return its parse function.
    Accepts bank names with any case (icici, Icici, ICICI).
    """
    module_name = f"custom_parsers.{bank.lower()}_parser"
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        raise ImportError(f"Could not import parser module '{module_name}': {e}")
    if not hasattr(mod, "parse"):
        raise AttributeError(f"Module '{module_name}' does not expose a parse(pdf_path) function")
    return mod.parse


def run_demo(bank: str, show_head: int = 5, compare: bool = True):
    print(f"\n=== Demo: running parser for bank '{bank}' ===")
    pdf_path, csv_path = make_paths(bank)

    print(f"Looking for PDF: {pdf_path}")
    print(f"Looking for CSV: {csv_path}")

    if not pdf_path.exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return 1
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        return 1

    try:
        parse = import_parser(bank)
    except Exception as e:
        print(f"❌ Failed to load parser: {e}")
        return 2

    print("▶ Running parser...")
    try:
        result_df = parse(str(pdf_path))
    except Exception as e:
        print(f"❌ Parser raised an exception: {e}")
        return 3

    if result_df is None:
        print("⚠️ Parser returned None.")
        return 4

    if not isinstance(result_df, pd.DataFrame):
        print(f"⚠️ Parser returned type {type(result_df)}, expected pandas.DataFrame")
        return 4

    print(f"✅ Parser produced DataFrame with {len(result_df)} rows and columns: {list(result_df.columns)}")
    print("\nSample parsed rows:")
    try:
        print(result_df.head(show_head).to_string(index=False))
    except Exception:
        print(result_df.head(show_head))

    # Optionally compare to expected CSV
    if compare:
        try:
            expected_df = pd.read_csv(csv_path)
            print(f"\nLoaded expected CSV with {len(expected_df)} rows and columns: {list(expected_df.columns)}")
        except Exception as e:
            print(f"❌ Failed to read expected CSV: {e}")
            return 5

        # Quick checks
        cols_match = list(result_df.columns) == list(expected_df.columns)
        rows_match = len(result_df) == len(expected_df)

        print(f"\nComparison summary:")
        print(f"  Columns identical: {cols_match}")
        print(f"  Row count equal:   {rows_match}")

        # Full equality check with relaxed dtype checking
        try:
            pd.testing.assert_frame_equal(
                result_df.reset_index(drop=True),
                expected_df.reset_index(drop=True),
                check_dtype=False,
            )
            print("🎉 Full comparison passed: parsed DataFrame matches expected CSV (values match ignoring dtype).")
        except AssertionError as ae:
            print("⚠️ Full comparison failed: parsed DataFrame does not exactly match expected CSV.")
            print("   Reason:", str(ae).splitlines()[0])
            # Give a small diff preview
            print("\nParsed head vs Expected head (parsed | expected):")
            parsed_head = result_df.head(show_head).astype(str)
            expected_head = expected_df.head(show_head).astype(str)
            for i in range(min(len(parsed_head), len(expected_head))):
                parsed_row = " | ".join(parsed_head.iloc[i].tolist())
                expected_row = " | ".join(expected_head.iloc[i].tolist())
                print(f"  {i+1:02d}: {parsed_row}  ||  {expected_row}")

    # Save output CSV copy for convenience
    out_csv = pdf_path.with_name(f"{bank}_sample_parsed_out.csv")
    try:
        result_df.to_csv(out_csv, index=False)
        print(f"\nSaved parsed output to: {out_csv}")
    except Exception as e:
        print(f"\n⚠️ Could not save parsed output CSV: {e}")

    return 0


def usage_instructions():
    print("\nHow to run this demo:")
    print("  python demo_run_parser.py --bank icici")
    print("Notes:")
    print("  - Ensure sample files are at data/<bank>/<bank>_sample.pdf and .csv")
    print("  - To avoid LLM calls during testing, run the agent with attempts_left set to 1 in agent.py\n")


def main():
    parser = argparse.ArgumentParser(description="Demo runner for bank statement parsers")
    parser.add_argument("--bank", "-b", default="icici", help="Bank name (folder and parser name). Default: icici")
    parser.add_argument("--rows", "-r", type=int, default=5, help="Number of sample rows to show")
    parser.add_argument("--no-compare", dest="compare", action="store_false", help="Do not compare parser output to expected CSV")
    args = parser.parse_args()

    show_architecture()
    show_project_layout()
    usage_instructions()

    rc = run_demo(args.bank.lower(), show_head=args.rows, compare=args.compare)
    if rc == 0:
        print("\nDemo completed successfully.")
    else:
        print("\nDemo finished with return code:", rc)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
