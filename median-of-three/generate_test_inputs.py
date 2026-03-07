"""
generate_test_inputs.py — Generate random and sorted CSV test input files for quicksort.

Creates a 'test_input/' directory and populates it with pairs of files for each
power of 10 from 10^0 (1) to 10^7 (10,000,000):

  test_input/
    one_random_ints.csv
    one_sorted_ints.csv
    ten_random_ints.csv
    ten_sorted_ints.csv
    one_hundred_random_ints.csv
    one_hundred_sorted_ints.csv
    ... and so on up to ten_million_*

Usage:
  python generate_test_inputs.py
"""

import os
import subprocess
import sys

# ---------------------------------------------------------------------------
# English names for each power of 10 from 10^0 to 10^7
# ---------------------------------------------------------------------------
NAMES = {
    1:          "one",
    10:         "ten",
    100:        "one_hundred",
    1_000:      "one_thousand",
    10_000:     "ten_thousand",
    100_000:    "one_hundred_thousand",
    1_000_000:  "one_million",
    10_000_000: "ten_million",
}

OUTPUT_DIR = "test_input"
GENERATOR  = "generate_random_ints_csv.py"


def generate_file(n, filename, extra_args=None):
    """
    Call generate_random_ints_csv.py via subprocess to produce a CSV file.

    Args:
        n:          Number of integers to generate.
        filename:   Destination file path to write the output to.
        extra_args: Optional list of extra CLI flags to pass to the generator
                    (e.g. ['--sorted'] or ['--reverse']).
    """
    cmd = [sys.executable, GENERATOR, str(n)] + (extra_args or [])

    # Run the generator and capture its stdout (the comma-separated integers)
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ERROR running generator: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    with open(filename, "w") as fh:
        fh.write(result.stdout)


def main():
    # Create the output directory if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: '{OUTPUT_DIR}/'")
    print()

    for exponent in range(8):          # 0 through 7  →  10^0 … 10^7
        n    = 10 ** exponent
        name = NAMES[n]

        random_file = os.path.join(OUTPUT_DIR, f"{name}_random_ints.csv")
        sorted_file = os.path.join(OUTPUT_DIR, f"{name}_sorted_ints.csv")

        print(f"Generating n={n:>10,}  ({name})")

        print(f"  -> {random_file}")
        generate_file(n, random_file)               # no extra flags → random

        print(f"  -> {sorted_file}")
        generate_file(n, sorted_file, ["--sorted"]) # --sorted → 1..n in order

    print()
    print("Done.")


if __name__ == "__main__":
    main()
