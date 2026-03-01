# Baseball Free-Agent Signing

A dynamic programming solution to the free-agent signing problem (CLRS 14-12).

Given a budget and a pool of players across multiple positions, maximize total WAR (Wins Above Replacement) without exceeding the budget. At most one player may be signed per position.

## Files

- `gen_players.py` — generates a random input file in JSON format
- `gen_batch.py` — generates a prepared suite of 30 test input files at various sizes
- `baseball.py` — reads the JSON and solves the problem

---

## Running the App

### From stdin (pipe)

```bash
python gen_players.py 20 100000000 | python baseball.py
```

### From a saved file using `--file` / `-f`

```bash
python baseball.py --file input.json
python baseball.py -f input.json
```

### Flags

| Flag | Short | Description |
|---|---|---|
| `--file <path>` | `-f` | Read input from a file instead of stdin |
| `--memo` | `-m` | Use the memoized solver instead of brute force |
| `--debug` | `-d` | Print verbose debug output including all players and solver trace |

Flags can be combined freely:

```bash
python baseball.py -f input.json -m -d
```

---

## Generating Input

### Manually with `gen_players.py`

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

### In bulk with `gen_batch.py`

```bash
python gen_batch.py
```

This runs `gen_players.py` 30 times, once for each odd number from 1 to 59 (`n = 1, 3, 5, ..., 59`). Each run uses a budget of roughly `n * $2,000,000` jittered by ±20% and rounded to the nearest $100,000. All files are saved to a `test_inputs/` subdirectory and named `{n}_players_{y}M.json`, for example `15_players_31M.json`. This gives you a ready-made suite of inputs ranging from trivially small to moderately challenging, useful for running benchmarks or regression tests across a range of problem sizes.

---

## Choosing `maximum_cost`

Since player costs range from $100,000 to $30,000,000 with an average around $15,000,000, the budget you set has a big effect on how constrained the problem is.

| Budget | Example | Behavior |
|---|---|---|
| **Tight** | $30M–$50M | Can only sign 2–3 players total. Forces hard tradeoffs and stress-tests the solver. |
| **Moderate** | $100M–$150M | Can sign roughly 6–10 players. Interesting middle ground where position coverage and WAR both matter. |
| **Loose** | $300M+ | Can likely afford one player at every position. Useful for sanity-checking that the algorithm always picks the highest WAR at each position. |

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

## Brute Force vs. Memoization

### Brute Force (default)

Without any flags, the solver uses a recursive brute force approach. For each player it considers two branches: sign them or skip them. If signed, all other players at the same position are eliminated from the remaining subproblem. This explores the full decision tree and is guaranteed to find the optimal solution, but the number of subproblems grows exponentially with `n`.

### Memoized (`--memo` / `-m`)

```bash
python baseball.py -f input.json --memo
```

The memoized solver uses the same recursive logic but caches the result of every subproblem it solves. A subproblem is uniquely identified by the pair of `(set of remaining players, remaining budget)`. If the solver encounters the same pair again via a different path through the decision tree, it returns the cached result immediately instead of recomputing it.

The key insight is that many different orderings of "skip player A, skip player B, ..." converge to the same remaining subproblem. Without memoization, each of those paths recomputes the answer from scratch. With memoization, the first path to reach a subproblem pays the cost; every subsequent path gets the answer for free.

---

## Performance Analysis

Tested on a MacBook Air M2.

| `n` | Brute Force | Memoized |
|---|---|---|
| 45 players | ~3 minutes | ~10 seconds |

At 45 players the brute force solver takes close to 3 minutes because the decision tree has an enormous number of overlapping subproblems that get recomputed repeatedly. Memoization reduces this to about 10 seconds — roughly an 18x speedup — by ensuring each unique subproblem is solved at most once. The improvement becomes more dramatic as `n` grows, since the number of overlapping subproblems increases much faster than linearly with the input size.

---

## Quick Start

```bash
# Small, inspectable run
python gen_players.py 20 100000000 | python baseball.py

# Same run with memoization
python gen_players.py 20 100000000 | python baseball.py --memo

# Save a file and run both solvers on the same input for comparison
python gen_players.py 45 90000000 > input.json
python baseball.py -f input.json
python baseball.py -f input.json --memo

# Generate the full test suite
python gen_batch.py

# Run the memoized solver on a batch file
python baseball.py -f test_inputs/45_players_90M.json --memo
```

---

---

## Complexity Analysis

Let **n** = number of players and **K** = `maximum_cost / 100,000` (the number of discrete budget units, since all costs are multiples of $100,000).

### Brute Force

**Time: O(n · 2ⁿ)**

At each recursive call the algorithm picks one player and branches into two subproblems: skip them, or sign them. This produces a binary decision tree of depth at most n, giving 2ⁿ leaf nodes and O(2ⁿ) total nodes. At each node the algorithm does O(n) work to filter the remaining player set. No results are cached, so overlapping subproblems — subproblems that are reached via multiple different paths through the tree — are recomputed from scratch every time.

**Space: O(n²)**

The recursion stack goes at most n levels deep. At each level a filtered copy of the remaining player set is held in memory, shrinking by at least one player per level. The total memory across the call stack at any one time is O(n) + O(n-1) + ... + O(1) = O(n²).

---

### Memoized

**Time: O(n · 2ⁿ · K) worst case — substantially better in practice**

The memo table is keyed on `(frozenset of remaining players, remaining budget)`. In the theoretical worst case — all n players at distinct positions with no budget constraints eliminating branches — there are up to 2ⁿ distinct player subsets and K distinct budget values, giving O(2ⁿ · K) unique subproblems each requiring O(n) work, for O(n · 2ⁿ · K) total.

In practice the improvement is dramatic. The position constraint is the key: signing any player at position P eliminates every other player at position P from all descendant subproblems. This means many branches of the tree collapse to the same remaining set far sooner than the worst case suggests. On a MacBook Air M2 with n=45 players, brute force took ~3 minutes while memoization took ~10 seconds — an ~18x speedup — and the gap widens as n grows.

**Space: O(n · 2ⁿ · K)**

The memo table stores one entry per unique subproblem. Each entry holds a set of up to n players. In the worst case this is O(n) per entry times O(2ⁿ · K) entries. In practice the number of reachable subproblems is far smaller due to the position constraint, so actual memory usage is much lower than the theoretical bound.

---

### Summary

| | Brute Force | Memoized |
|---|---|---|
| **Time** | O(n · 2ⁿ) | O(n · 2ⁿ · K) worst case, much less in practice |
| **Space** | O(n²) | O(n · 2ⁿ · K) worst case |
| **n=45 on M2** | ~3 minutes | ~10 seconds |

The memoized solver trades memory for time. The brute force solver uses very little memory but recomputes overlapping subproblems repeatedly. For any n above ~25 the memoized solver is the clear practical choice.