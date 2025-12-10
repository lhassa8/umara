#!/usr/bin/env python3
"""
Run All Umara Benchmarks

Executes all benchmark suites and generates a comprehensive report.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from benchmarks.core import BenchmarkRunner


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n")
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)


def run_all_benchmarks():
    """Run all benchmark suites."""
    start_time = time.time()

    print("\n" + "=" * 70)
    print("  UMARA PERFORMANCE BENCHMARK SUITE")
    print("  Comparing Umara vs Streamlit Architecture")
    print("=" * 70)

    all_results = []

    # Component Creation
    print_header("1. COMPONENT CREATION")
    from benchmarks.test_component_creation import run_benchmarks as run_component
    all_results.append(("Component Creation", run_component()))

    # Tree Diffing
    print_header("2. TREE DIFFING (Umara's Key Advantage)")
    from benchmarks.test_tree_diffing import run_benchmarks as run_diffing
    all_results.append(("Tree Diffing", run_diffing()))

    # Serialization
    print_header("3. SERIALIZATION")
    from benchmarks.test_serialization import run_benchmarks as run_serial
    all_results.append(("Serialization", run_serial()))

    # Validation
    print_header("4. FORM VALIDATION (Umara Exclusive)")
    from benchmarks.test_validation import run_benchmarks as run_validation
    all_results.append(("Validation", run_validation()))

    # State Management
    print_header("5. STATE MANAGEMENT")
    from benchmarks.test_state_management import run_benchmarks as run_state
    all_results.append(("State Management", run_state()))

    # Final Summary
    end_time = time.time()

    print("\n")
    print("=" * 70)
    print("  FINAL SUMMARY")
    print("=" * 70)
    print(f"\nTotal benchmark time: {end_time - start_time:.2f} seconds")
    print(f"Suites executed: {len(all_results)}")

    # Key advantages summary
    print("\n" + "-" * 70)
    print("  UMARA'S KEY PERFORMANCE ADVANTAGES")
    print("-" * 70)

    advantages = [
        ("Incremental Updates", "Only changed components are sent to frontend"),
        ("WebSocket Protocol", "Persistent connection vs HTTP polling"),
        ("Lightweight Components", "Simple dataclasses vs Protocol Buffers"),
        ("Built-in Validation", "15+ validators with no extra setup"),
        ("Fragment Reruns", "Partial page updates without full rerun"),
        ("Computed State", "Reactive derived values with auto-caching"),
        ("True Streaming", "Real-time token display with metrics"),
    ]

    for name, description in advantages:
        print(f"\n  {name}")
        print(f"    {description}")

    print("\n" + "=" * 70)
    print("  Benchmarks complete!")
    print("=" * 70 + "\n")

    return all_results


if __name__ == "__main__":
    run_all_benchmarks()
