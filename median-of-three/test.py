"""
test_quicksort.py — Test harness for quicksort.py

Runs quicksort.py as a subprocess, captures its stdout (the sorted output),
and asserts it matches Python's built-in sorted() for a variety of inputs:

  - Array types : random, sorted ascending, sorted descending, single element,
                  duplicates, already-sorted (already in order), all identical
  - Sizes       : 1, 2, 5, 10, 20, 50, 99  (all < 100)
  - Partitions  : 'default' and 'median-of-three'

Usage:
  python test_quicksort.py           # run all tests, print summary
  python test_quicksort.py -v        # verbose: print each test case

The harness does NOT use --suppress so that it captures and validates the
actual sorted output written to stdout.
"""

import subprocess
import sys
import random
import unittest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

QUICKSORT_SCRIPT = "quicksort.py"
PARTITIONS = ["default", "median-of-three"]


def run_quicksort(numbers: list[int], partition: str) -> list[int]:
    """
    Run quicksort.py on the given list of integers using the specified
    partition method.  Returns the sorted output as a list of integers.

    The input is passed via stdin as a comma-separated string.
    --suppress is NOT used so that we can capture and validate the output.
    --trace is NOT used to keep stdout clean for parsing.

    Raises AssertionError if the process exits with a non-zero return code.
    """
    input_str = ",".join(map(str, numbers))
    cmd = [sys.executable, QUICKSORT_SCRIPT, "--partition", partition]

    result = subprocess.run(
        cmd,
        input=input_str,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"quicksort.py exited with code {result.returncode}\n"
        f"stderr: {result.stderr.strip()}"
    )

    # stdout is a single line of comma-separated integers
    output = result.stdout.strip()
    assert output, "quicksort.py produced no output (did you accidentally pass --suppress?)"

    return list(map(int, output.split(",")))


def make_random(size: int, lo: int = 1, hi: int = 100_000) -> list[int]:
    """Return a list of `size` random integers in [lo, hi]."""
    return [random.randint(lo, hi) for _ in range(size)]


def make_sorted(size: int) -> list[int]:
    """Return a sorted list 1, 2, ..., size."""
    return list(range(1, size + 1))


def make_reverse(size: int) -> list[int]:
    """Return a reverse-sorted list size, size-1, ..., 1."""
    return list(range(size, 0, -1))


def make_duplicates(size: int) -> list[int]:
    """Return a list of `size` integers chosen from a small pool (forces duplicates)."""
    pool = list(range(1, max(3, size // 3) + 1))
    return [random.choice(pool) for _ in range(size)]


def make_identical(size: int, value: int = 42) -> list[int]:
    """Return a list of `size` identical values."""
    return [value] * size


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

SIZES = [1, 2, 5, 10, 20, 50, 99]


class TestQuickSort(unittest.TestCase):
    """Each test method covers one array type across all sizes and partitions."""

    def _assert_sorted(self, numbers: list[int], partition: str, label: str):
        """
        Core assertion: run quicksort on `numbers` with `partition` and check
        that the output matches Python's sorted().
        """
        expected = sorted(numbers)
        actual   = run_quicksort(numbers, partition)
        self.assertEqual(
            actual, expected,
            msg=(
                f"\nFAIL  partition={partition}  {label}\n"
                f"  input    : {numbers}\n"
                f"  expected : {expected}\n"
                f"  got      : {actual}"
            )
        )

    # --- Random arrays -------------------------------------------------------

    def test_random_default(self):
        """Random arrays with default (last-element) partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_random(size)
                self._assert_sorted(numbers, "default", f"random n={size}")

    def test_random_median_of_three(self):
        """Random arrays with median-of-three partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_random(size)
                self._assert_sorted(numbers, "median-of-three", f"random n={size}")

    # --- Sorted ascending arrays ---------------------------------------------

    def test_sorted_asc_default(self):
        """
        Already-sorted (ascending) arrays with default partition.
        This is the worst-case O(n²) input for the default partition.
        Still small enough (n < 100) to complete quickly.
        """
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_sorted(size)
                self._assert_sorted(numbers, "default", f"sorted-asc n={size}")

    def test_sorted_asc_median_of_three(self):
        """Already-sorted (ascending) arrays with median-of-three partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_sorted(size)
                self._assert_sorted(numbers, "median-of-three", f"sorted-asc n={size}")

    # --- Sorted descending arrays --------------------------------------------

    def test_sorted_desc_default(self):
        """
        Reverse-sorted arrays with default partition.
        Also a worst-case input for the default partition.
        """
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_reverse(size)
                self._assert_sorted(numbers, "default", f"sorted-desc n={size}")

    def test_sorted_desc_median_of_three(self):
        """Reverse-sorted arrays with median-of-three partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_reverse(size)
                self._assert_sorted(numbers, "median-of-three", f"sorted-desc n={size}")

    # --- Arrays with duplicate values ----------------------------------------

    def test_duplicates_default(self):
        """Arrays with many duplicate values — default partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_duplicates(size)
                self._assert_sorted(numbers, "default", f"duplicates n={size}")

    def test_duplicates_median_of_three(self):
        """Arrays with many duplicate values — median-of-three partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_duplicates(size)
                self._assert_sorted(numbers, "median-of-three", f"duplicates n={size}")

    # --- All-identical arrays ------------------------------------------------

    def test_identical_default(self):
        """Arrays where every element is the same — default partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_identical(size)
                self._assert_sorted(numbers, "default", f"identical n={size}")

    def test_identical_median_of_three(self):
        """Arrays where every element is the same — median-of-three partition."""
        for size in SIZES:
            with self.subTest(size=size):
                numbers = make_identical(size)
                self._assert_sorted(numbers, "median-of-three", f"identical n={size}")

    # --- Two-element arrays (edge case) --------------------------------------

    def test_two_elements(self):
        """Two-element arrays in both orders — both partitions."""
        for partition in PARTITIONS:
            for numbers in ([1, 2], [2, 1]):
                with self.subTest(partition=partition, numbers=numbers):
                    self._assert_sorted(numbers, partition, f"two-element {numbers}")

    # --- Single-element array (edge case) ------------------------------------

    def test_single_element(self):
        """A single element — both partitions."""
        for partition in PARTITIONS:
            with self.subTest(partition=partition):
                self._assert_sorted([42], partition, "single element")

    # --- Negative numbers ----------------------------------------------------

    def test_negative_numbers(self):
        """Arrays containing negative integers — both partitions."""
        for partition in PARTITIONS:
            for size in [5, 20, 50]:
                with self.subTest(partition=partition, size=size):
                    numbers = [random.randint(-50_000, 50_000) for _ in range(size)]
                    self._assert_sorted(numbers, partition, f"negatives n={size}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Seed random for reproducibility when running without -v
    random.seed(42)
    unittest.main(verbosity=2)