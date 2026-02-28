#!/usr/bin/env python3
"""
Usage: python gen_players.py <n> <maximum_cost>

Generates n random baseball free-agent players and prints them as JSON to stdout.
Positions are randomly drawn from a random subset of labels A-Z, AA, AB, ... (9 to 30 positions).
"""

import json
import random
import string
import sys


def generate_positions() -> list[str]:
    count = random.randint(9, 30)
    all_labels = []
    i = 0
    while len(all_labels) < count:
        name = ""
        n = i
        while True:
            name = string.ascii_uppercase[n % 26] + name
            n = n // 26 - 1
            if n < 0:
                break
        all_labels.append(name)
        i += 1
    return all_labels


FIRST_NAMES = ["Carlos", "Mike", "Jake", "Luis", "Aaron", "Shohei", "Freddie", "Mookie", "Nolan", "Bryce"]
LAST_NAMES = ["Smith", "Johnson", "Garcia", "Martinez", "Rodriguez", "Lopez", "Hernandez", "Lee", "Walker", "Hall"]


def random_player(index: int, positions: list[str]) -> dict:
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last} {index}"

    position = random.choice(positions)
    cost = random.randint(1, 300) * 100_000
    war = round(random.uniform(-1.0, 10.0), 1)

    return {
        "name": name,
        "position": position,
        "cost": cost,
        "war": war,
    }


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <n> <maximum_cost>", file=sys.stderr)
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print(f"Error: <n> must be an integer, got {sys.argv[1]!r}", file=sys.stderr)
        sys.exit(1)

    try:
        maximum_cost = int(sys.argv[2])
    except ValueError:
        print(f"Error: <maximum_cost> must be an integer, got {sys.argv[2]!r}", file=sys.stderr)
        sys.exit(1)

    if n < 0:
        print("Error: <n> must be non-negative", file=sys.stderr)
        sys.exit(1)

    if maximum_cost < 0:
        print("Error: <maximum_cost> must be non-negative", file=sys.stderr)
        sys.exit(1)

    positions = generate_positions()
    players = [random_player(i, positions) for i in range(n)]
    output = {
        "maximum_cost": maximum_cost,
        "players": players,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
