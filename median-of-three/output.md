# Quicksort Benchmark Results

Each cell shows wall-clock time for sorting that input with `--suppress` (output discarded).
Java was run with `-Xss64m` to provide sufficient stack space for deep recursion.

## Random Input

| Implementation | 1 | 10 | 100 | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|---|---|---|
| Java (default) | 0.282s | 0.127s | 0.141s | 0.143s | 0.147s | 0.159s | 0.229s |
| Java (median-of-three) | 0.129s | 0.134s | 0.134s | 0.139s | 0.139s | 0.154s | 0.225s |

## Sorted Input

| Implementation | 1 | 10 | 100 | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|---|---|---|
| Java (default) | 0.139s | 0.140s | 0.141s | 0.145s | 0.157s | 0.751s | 53.136s |
| Java (median-of-three) | 0.136s | 0.136s | 0.135s | 0.137s | 0.140s | 0.149s | 0.187s |

