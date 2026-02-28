# Baseball Free-Agent Signing

A dynamic programming solution to the free-agent signing problem (CLRS 14-12). 

Given a budget and a pool of players across multiple positions, maximize total WAR (Wins Above Replacement) without exceeding the budget. At most one player may be signed per position.

## Files

- `gen_players.py` — generates a random input file in JSON format
- `baseball.py` — reads the JSON and solves the problem

---

## Generating Input

```bash
python gen_players.py <n> <maximum_cost>
```

This prints a JSON object to stdout with two keys:
- `maximum_cost` — the budget passed in as an argument
- `players` — an array of `n` randomly generated players, each with a `name`, `position`, `cost`, and `war`

Positions are drawn from a randomly sized pool of labels (`A`, `B`, ..., `Z`, `AA`, `AB`, ...) with between 9 and 30 distinct positions generated per run.

Player costs are random multiples of $100,000 between $100,000 and $30,000,000.

To save the output to a file:

```bash
python gen_players.py 20 100000000 > input.json
```

---

## Running the App

Pipe the generator directly into the app:

```bash
python gen_players.py 20 100000000 | python baseball.py
```

Or run from a saved file:

```bash
python baseball.py < input.json
```

---

## Choosing `maximum_cost`

Since player costs range from $100,000 to $30,000,000 with an average around $15,000,000, the budget you set has a big effect on how constrained the problem is.

| Budget | Example | Behavior |
|---|---|---|
| **Tight** | $30,000,000–$50,000,000 | Can only sign 2–3 players total. Forces hard tradeoffs and stress-tests the DP logic. |
| **Moderate** | $100,000,000–$150,000,000 | Can sign roughly 6–10 players. Interesting middle ground where position coverage and WAR both matter. |
| **Loose** | $300,000,000+ | Can likely afford one player at every position. Useful for sanity-checking that the algorithm always picks the highest WAR at each position. |

A good default for general testing is **$100,000,000**.

---

## Choosing `n` (Number of Players)

`n` is the total number of players in the pool spread across all positions. Since the number of positions is between 9 and 30, the ratio of players to positions determines how much meaningful choice the algorithm has.

| `n` | Behavior |
|---|---|
| **< 15** | Sparse pool — many positions may have only one candidate or none. Useful for edge case testing. |
| **20–50** | Good range for development and debugging. Enough variety without being hard to inspect by hand. |
| **100–300** | Realistic pool size. Tests algorithm performance and is large enough that you can't reason through the answer manually. |
| **1000+** | Stress test for runtime and memory. Useful once the implementation is correct and you want to validate complexity. |

A good default for getting started is **`n = 20`** with a moderate budget, then scale up to `n = 100` once the algorithm is working.

---

## Quick Start

```bash
# Small, inspectable run
python gen_players.py 20 100000000 | python baseball.py

# Tight budget stress test
python gen_players.py 50 30000000 | python baseball.py

# Large scale test
python gen_players.py 300 100000000 | python baseball.py
```
