#!/usr/bin/env python3
"""
Usage: python gen_players.py <n> <maximum_cost>

Generates n random baseball free-agent players and prints them as JSON to stdout.
Positions are randomly drawn from a random subset of labels A-Z, AA, AB, ... (9 to 30 positions).
The sum of all player costs is guaranteed to exceed maximum_cost.
"""

import json
import random
import string
import sys

FIRST_NAMES = [
    "Aaron", "Abel", "Adam", "Adrian", "Alejandro", "Alex", "Andre", "Angel", "Anthony", "Antonio",
    "Bryce", "Brandon", "Brett", "Brian", "Bruno", "Byron", "Caleb", "Carlos", "Casey", "Chad",
    "Chris", "Clay", "Cole", "Colin", "Connor", "Corey", "Curtis", "Dale", "Damian", "Daniel",
    "Darius", "David", "Derek", "Diego", "Dominic", "Drew", "Dylan", "Eduardo", "Eli", "Elias",
    "Emilio", "Eric", "Ethan", "Evan", "Felix", "Fernando", "Freddie", "Gabriel", "Garrett", "Gavin",
    "Gerardo", "Grant", "Greg", "Hector", "Hunter", "Ian", "Isaac", "Ivan", "Jack", "Jacob",
    "Jake", "Jalen", "James", "Jason", "Javier", "Jesse", "Joel", "Jorge", "Jose", "Josh",
    "Juan", "Julian", "Justin", "Kevin", "Kyle", "Lance", "Leo", "Logan", "Lorenzo", "Lucas",
    "Luis", "Marcus", "Mario", "Matt", "Miguel", "Mike", "Mookie", "Nathan", "Nick", "Nolan",
    "Omar", "Oscar", "Pablo", "Patrick", "Pedro", "Rafael", "Ramon", "Ricardo", "Roberto", "Ryan",
    "Salvador", "Sam", "Santiago", "Scott", "Sean", "Shohei", "Spencer", "Tanner", "Taylor", "Trevor",
]

LAST_NAMES = [
    "Acosta", "Adams", "Aguilar", "Alvarez", "Anderson", "Bautista", "Bell", "Beltran", "Benintendi", "Betts",
    "Bogaerts", "Bregman", "Brown", "Bryant", "Buxton", "Cabrera", "Cano", "Carter", "Castillo", "Chapman",
    "Clark", "Cole", "Collins", "Contreras", "Cooper", "Correa", "Crawford", "Cruz", "Davis", "Devers",
    "Diaz", "Doan", "Donaldson", "Dozier", "Duran", "Estrada", "Farmer", "Fernandez", "Flores", "Franco",
    "Freeman", "Galvis", "Garcia", "Gallo", "Goldschmidt", "Gomez", "Gonzalez", "Gordon", "Green", "Guerrero",
    "Hall", "Hamilton", "Harper", "Harris", "Henderson", "Hernandez", "Hill", "Hoskins", "Howard", "Jackson",
    "James", "Jimenez", "Johnson", "Jones", "Judge", "Kim", "King", "Kirk", "Lee", "Leon",
    "Lewis", "Lindor", "Lopez", "Lowe", "Machado", "Martin", "Martinez", "Meadows", "Merrifield", "Miller",
    "Mitchell", "Molina", "Moore", "Morales", "Muncy", "Murphy", "Myers", "Nido", "Nimmo", "Nunez",
    "Olson", "Ortiz", "Ozuna", "Pena", "Perez", "Pollack", "Ramirez", "Reyes", "Reynolds", "Rivera",
    "Roberts", "Rodriguez", "Rogers", "Rojas", "Rosario", "Sanchez", "Santana", "Semien", "Smith", "Soto",
    "Springer", "Stanton", "Suarez", "Swanson", "Tatis", "Taylor", "Thomas", "Thompson", "Torres", "Turner",
    "Urias", "Urshela", "Vientos", "Villar", "Voit", "Walker", "Walsh", "White", "Williams", "Wilson",
]


def generate_positions() -> list[str]:
    count = random.randint(9, 30)
    all_labels: list[str] = []
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


def generate_names(n: int) -> list[str]:
    all_combos = [f"{f} {l}" for f in FIRST_NAMES for l in LAST_NAMES]
    random.shuffle(all_combos)
    names: list[str] = []
    for i in range(n):
        names.append(all_combos[i % len(all_combos)])
    return names


def random_player(name: str, index: int, positions: list[str]) -> dict[str, object]:
    position = random.choice(positions)
    cost = random.randint(1, 300) * 100_000
    war = round(random.uniform(-1.0, 10.0), 1)
    return {"name": f"{name} {index}", "position": position, "cost": cost, "war": war}


def ensure_total_exceeds_budget(
    players: list[dict[str, object]], maximum_cost: int
) -> list[dict[str, object]]:
    total = sum(int(p["cost"]) for p in players)  # type: ignore[arg-type]
    if total > maximum_cost:
        return players

    shortfall = maximum_cost - total + 100_000
    while shortfall > 0:
        target = random.randrange(len(players))
        bump = min(shortfall, random.randint(1, 10) * 100_000)
        players[target]["cost"] = int(players[target]["cost"]) + bump  # type: ignore[operator]
        shortfall -= bump

    return players


def main() -> None:
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

    if n <= 0:
        print("Error: <n> must be a positive integer", file=sys.stderr)
        sys.exit(1)

    if maximum_cost < 0:
        print("Error: <maximum_cost> must be non-negative", file=sys.stderr)
        sys.exit(1)

    positions = generate_positions()
    names = generate_names(n)
    players = [random_player(names[i], i, positions) for i in range(n)]
    players = ensure_total_exceeds_budget(players, maximum_cost)

    output = {"maximum_cost": maximum_cost, "players": players}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
