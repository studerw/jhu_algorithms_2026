"""
benchmark.py — Time Python and Java quicksort implementations across all test inputs.

Runs four configurations against every file in test_input/:
  - Python  + default partition
  - Python  + median-of-three partition
  - Java    + default partition
  - Java    + median-of-three partition

Results are written to output.md as a formatted markdown table where each row is
one (implementation, partition) combination and each column is an input size.
"""

import os
import subprocess
import sys
import time

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TEST_INPUT_DIR  = "test_input"
OUTPUT_FILE     = "output.md"
PYTHON          = sys.executable
JAVA            = "java"
JAVA_STACK_FLAG = "-Xss512m"

# The four benchmark configurations: (label, command_template)
# {file} will be substituted with the actual input file path
CONFIGS = [
    # (
    #     "Python (default)",
    #     [PYTHON, "quicksort.py", "--suppress", "--partition", "default", "-f", "{file}"]
    # ),
    # (
    #     "Python (median-of-three)",
    #     [PYTHON, "quicksort.py", "--suppress", "--partition", "median-of-three", "-f", "{file}"]
    # ),
    (
        "Java (default)",
        [JAVA, JAVA_STACK_FLAG, "QuickSort", "--suppress", "--partition", "default", "-f", "{file}"]
    ),
    (
        "Java (median-of-three)",
        [JAVA, JAVA_STACK_FLAG, "QuickSort", "--suppress", "--partition", "median-of-three", "-f", "{file}"]
    ),
]

# Powers of 10 and their english names, in display order
SIZES = [
    (1,           "1",          "one"),
    (10,          "10",         "ten"),
    (100,         "100",        "one_hundred"),
    (1_000,       "1,000",      "one_thousand"),
    (10_000,      "10,000",     "ten_thousand"),
    (100_000,     "100,000",    "one_hundred_thousand"),
    (1_000_000,   "1,000,000",  "one_million"),
    # (10_000_000,  "10,000,000", "ten_million"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_cmd(template, filepath):
    """Substitute {file} placeholder in the command template with the actual path."""
    return [part.replace("{file}", filepath) for part in template]


def run_timed(cmd):
    """
    Run a command and return (elapsed_seconds, success).

    Times only the subprocess execution itself, not any Python overhead.
    Returns (None, False) if the process exits with a non-zero return code.
    """
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start

    if result.returncode != 0:
        print(f"    ERROR: {result.stderr.strip()[:120]}", file=sys.stderr)
        return None, False

    return elapsed, True


def fmt_time(seconds):
    """Format a duration for the markdown table (e.g. '1.234s' or 'ERROR')."""
    if seconds is None:
        return "ERROR"
    return f"{seconds:.3f}s"


def input_file(name, kind):
    """Build the path for a test input file, e.g. 'test_input/ten_thousand_random_ints.csv'."""
    return os.path.join(TEST_INPUT_DIR, f"{name}_{kind}_ints.csv")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # results[config_label][size_label][kind] = elapsed_seconds
    # kind is either 'random' or 'sorted'
    results = {label: {} for label, _ in CONFIGS}

    total_runs = len(CONFIGS) * len(SIZES) * 2  # 2 kinds: random + sorted
    run_number = 0

    for n, display, name in SIZES:
        for kind in ("random", "sorted"):
            filepath = input_file(name, kind)

            if not os.path.exists(filepath):
                print(f"WARNING: missing file {filepath}, skipping.", file=sys.stderr)
                for label, _ in CONFIGS:
                    results[label].setdefault(f"{display} ({kind})", None)
                continue

            for label, template in CONFIGS:
                run_number += 1
                cmd = build_cmd(template, filepath)
                print(f"[{run_number}/{total_runs}] {label:30s}  n={display:>12}  {kind}")

                elapsed, ok = run_timed(cmd)
                col = f"{display} ({kind})"
                results[label][col] = elapsed if ok else None

    # -----------------------------------------------------------------------
    # Build column list in insertion order
    # -----------------------------------------------------------------------
    columns = []
    for n, display, name in SIZES:
        for kind in ("random", "sorted"):
            col = f"{display} ({kind})"
            if col not in columns:
                columns.append(col)

    # -----------------------------------------------------------------------
    # Write markdown
    # -----------------------------------------------------------------------
    with open(OUTPUT_FILE, "w") as f:

        f.write("# Quicksort Benchmark Results\n\n")
        f.write(
            "Each cell shows wall-clock time for sorting that input with `--suppress` "
            "(output discarded).\n"
            "Java was run with `-Xss64m` to provide sufficient stack space for deep recursion.\n\n"
        )

        # --- Summary table: rows = configs, columns = sizes ---
        # Split into two sub-tables (random and sorted) for readability

        for kind in ("random", "sorted"):
            kind_cols = [c for c in columns if c.endswith(f"({kind})")]
            # Header labels: strip the " (kind)" suffix for brevity
            headers = [c.replace(f" ({kind})", "") for c in kind_cols]

            f.write(f"## {kind.capitalize()} Input\n\n")

            # Table header
            f.write("| Implementation | " + " | ".join(headers) + " |\n")
            f.write("|" + "---|" * (len(headers) + 1) + "\n")

            # One row per config
            for label, _ in CONFIGS:
                row_cells = [fmt_time(results[label].get(c)) for c in kind_cols]
                f.write(f"| {label} | " + " | ".join(row_cells) + " |\n")

            f.write("\n")

    print(f"\nResults written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
