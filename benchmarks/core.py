"""
Core benchmark infrastructure for Umara.

Provides timing, memory measurement, and comparison utilities.
"""

from __future__ import annotations

import gc
import json
import statistics
import sys
import time
import tracemalloc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""

    name: str
    framework: str  # "umara" or "streamlit"
    iterations: int
    times_ms: list[float] = field(default_factory=list)
    memory_kb: float = 0.0
    peak_memory_kb: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def mean_ms(self) -> float:
        """Average execution time in milliseconds."""
        return statistics.mean(self.times_ms) if self.times_ms else 0.0

    @property
    def median_ms(self) -> float:
        """Median execution time in milliseconds."""
        return statistics.median(self.times_ms) if self.times_ms else 0.0

    @property
    def std_ms(self) -> float:
        """Standard deviation of execution times."""
        return statistics.stdev(self.times_ms) if len(self.times_ms) > 1 else 0.0

    @property
    def min_ms(self) -> float:
        """Minimum execution time."""
        return min(self.times_ms) if self.times_ms else 0.0

    @property
    def max_ms(self) -> float:
        """Maximum execution time."""
        return max(self.times_ms) if self.times_ms else 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "framework": self.framework,
            "iterations": self.iterations,
            "mean_ms": self.mean_ms,
            "median_ms": self.median_ms,
            "std_ms": self.std_ms,
            "min_ms": self.min_ms,
            "max_ms": self.max_ms,
            "memory_kb": self.memory_kb,
            "peak_memory_kb": self.peak_memory_kb,
            "metadata": self.metadata,
        }


@dataclass
class BenchmarkComparison:
    """Comparison between Umara and Streamlit results."""

    name: str
    umara: BenchmarkResult
    streamlit: BenchmarkResult | None

    @property
    def speedup(self) -> float | None:
        """How much faster Umara is (>1 means Umara is faster)."""
        if not self.streamlit or self.umara.mean_ms == 0:
            return None
        return self.streamlit.mean_ms / self.umara.mean_ms

    @property
    def memory_reduction(self) -> float | None:
        """Memory reduction ratio (>1 means Umara uses less memory)."""
        if not self.streamlit or self.umara.memory_kb == 0:
            return None
        return self.streamlit.memory_kb / self.umara.memory_kb

    def summary(self) -> str:
        """Generate summary string."""
        lines = [f"Benchmark: {self.name}"]
        lines.append("-" * 50)
        lines.append(f"{'Metric':<20} {'Umara':<15} {'Streamlit':<15} {'Ratio':<10}")
        lines.append("-" * 50)

        st_mean = self.streamlit.mean_ms if self.streamlit else "N/A"
        speedup = f"{self.speedup:.2f}x" if self.speedup else "N/A"
        lines.append(
            f"{'Mean time (ms)':<20} {self.umara.mean_ms:<15.2f} {st_mean:<15} {speedup:<10}"
        )

        st_mem = self.streamlit.memory_kb if self.streamlit else "N/A"
        mem_ratio = f"{self.memory_reduction:.2f}x" if self.memory_reduction else "N/A"
        lines.append(
            f"{'Memory (KB)':<20} {self.umara.memory_kb:<15.1f} {st_mem:<15} {mem_ratio:<10}"
        )

        return "\n".join(lines)


class BenchmarkRunner:
    """Runs and manages benchmarks."""

    def __init__(self, warmup_iterations: int = 3, iterations: int = 100):
        self.warmup_iterations = warmup_iterations
        self.iterations = iterations
        self.results: list[BenchmarkResult] = []

    def time_function(
        self,
        func: Callable[[], Any],
        name: str,
        framework: str = "umara",
        iterations: int | None = None,
    ) -> BenchmarkResult:
        """
        Time a function's execution.

        Args:
            func: Function to benchmark
            name: Benchmark name
            framework: Framework being tested
            iterations: Number of iterations (uses default if None)

        Returns:
            BenchmarkResult with timing data
        """
        iters = iterations or self.iterations

        # Warmup
        for _ in range(self.warmup_iterations):
            func()

        # Force garbage collection
        gc.collect()

        # Start memory tracking
        tracemalloc.start()

        times_ms = []
        for _ in range(iters):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times_ms.append((end - start) * 1000)

        # Get memory stats
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        result = BenchmarkResult(
            name=name,
            framework=framework,
            iterations=iters,
            times_ms=times_ms,
            memory_kb=current / 1024,
            peak_memory_kb=peak / 1024,
        )

        self.results.append(result)
        return result

    def compare(
        self,
        umara_func: Callable[[], Any],
        streamlit_func: Callable[[], Any] | None,
        name: str,
    ) -> BenchmarkComparison:
        """
        Compare Umara and Streamlit implementations.

        Args:
            umara_func: Umara implementation to test
            streamlit_func: Streamlit implementation (optional)
            name: Benchmark name

        Returns:
            BenchmarkComparison with results
        """
        umara_result = self.time_function(umara_func, name, "umara")

        streamlit_result = None
        if streamlit_func:
            streamlit_result = self.time_function(streamlit_func, name, "streamlit")

        return BenchmarkComparison(
            name=name,
            umara=umara_result,
            streamlit=streamlit_result,
        )

    def save_results(self, path: str | Path) -> None:
        """Save results to JSON file."""
        path = Path(path)
        data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "python_version": sys.version,
            "warmup_iterations": self.warmup_iterations,
            "default_iterations": self.iterations,
            "results": [r.to_dict() for r in self.results],
        }
        path.write_text(json.dumps(data, indent=2))

    def print_summary(self) -> None:
        """Print summary of all results."""
        print("\n" + "=" * 60)
        print("BENCHMARK RESULTS SUMMARY")
        print("=" * 60 + "\n")

        # Group by name
        by_name: dict[str, list[BenchmarkResult]] = {}
        for r in self.results:
            if r.name not in by_name:
                by_name[r.name] = []
            by_name[r.name].append(r)

        for name, results in by_name.items():
            print(f"\n{name}")
            print("-" * 50)

            umara = next((r for r in results if r.framework == "umara"), None)
            streamlit = next((r for r in results if r.framework == "streamlit"), None)

            if umara:
                print(f"  Umara:     {umara.mean_ms:>8.2f} ms  (mem: {umara.memory_kb:.1f} KB)")
            if streamlit:
                print(f"  Streamlit: {streamlit.mean_ms:>8.2f} ms  (mem: {streamlit.memory_kb:.1f} KB)")

            if umara and streamlit and streamlit.mean_ms > 0:
                speedup = streamlit.mean_ms / umara.mean_ms
                indicator = "faster" if speedup > 1 else "slower"
                print(f"  -> Umara is {abs(speedup):.2f}x {indicator}")
