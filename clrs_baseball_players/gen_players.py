#!/usr/bin/env python3
"""
Usage: python gen_players.py <n>

Generates n random baseball free-agent players and prints them as JSON to stdout.
"""

import json
import random
import sys

POSITIONS = ["SP", "RP-L", "RP-R", "RP-S", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"]

FIRST_NAMES = ["Carlos", "Mike", "Jake", "Luis", "Aaron", "Shohei", "Freddie", "Mookie", "Nolan", "Bryce"]
LAST_NAMES = ["Smith", "Johnson", "Garcia", "Martinez", "Rodriguez", "Lopez", "Hernandez", "Lee", "Walker", "Hall"]


def random_player(index: int) -> dict:
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last} {index}"  # index ensures uniqueness

    position = random.choice(POSITIONS)

    # Cost is a multiple of $100,000, ranging from $100k to $30M
    cost_units = random.randint(1, 300)
    cost = cost_units * 100_000

    # WAR typically ranges from -1 to 10 for free agents worth considering
    war = round(random.uniform(-1.0, 10.0), 1)

    return {
        "name": name,
        "position": position,
        "cost": cost,
        "war": war,
    }


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <n>", file=sys.stderr)
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print(f"Error: <n> must be an integer, got {sys.argv[1]!r}", file=sys.stderr)
        sys.exit(1)

    if n < 0:
        print("Error: <n> must be non-negative", file=sys.stderr)
        sys.exit(1)

    players = [random_player(i) for i in range(n)]
    print(json.dumps(players, indent=2))


if __name__ == "__main__":
    main()
