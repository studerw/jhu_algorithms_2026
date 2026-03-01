#!/usr/bin/env python3
"""
Runs gen_players.py 30 times for n = 1, 3, 5, ..., 59 players.
Budget is roughly n * $2,000,000 with some random noise.
Output files are named {n}_players_{y}M.json in the ./test_inputs/ directory.
"""

import os
import random
import subprocess
import sys


OUTPUT_DIR = "test_inputs"


def budget_for(n: int) -> int:
    # Base is n * $2,000,000, jittered by +/- 20%
    base = n * 2_000_000
    jitter = random.uniform(0.8, 1.2)
    # Round to nearest $100,000 to stay consistent with player cost granularity
    return round(base * jitter / 100_000) * 100_000


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Odd numbers 1, 3, 5, ..., 59 gives exactly 30 values
    player_counts = list(range(1, 60, 2))

    for n in player_counts:
        budget = budget_for(n)
        millions = budget // 1_000_000
        filename = os.path.join(OUTPUT_DIR, f"{n}_players_{millions}M.json")

        result = subprocess.run(
            [sys.executable, "gen_players.py", str(n), str(budget)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"ERROR generating n={n}: {result.stderr}", file=sys.stderr)
            continue

        with open(filename, "w") as f:
            f.write(result.stdout)

        print(f"Generated {filename}  (budget: ${budget:,})")


if __name__ == "__main__":
    main()