# Quicksort Benchmark Results

Each cell shows wall-clock time for sorting that input with `--suppress` (output discarded).
Java was run with `-Xss64m` to provide sufficient stack space for deep recursion.

## Random Input

| Implementation | 1 | 10 | 100 | 1,000 | 10,000 | 100,000 |
|---|---|---|---|---|---|---|
| Python (default) | 0.025s | 0.021s | 0.021s | 0.022s | 0.031s | 0.143s |
| Python (median-of-three) | 0.021s | 0.021s | 0.021s | 0.022s | 0.030s | 0.134s |
| Java (default) | 0.328s | 0.091s | 0.092s | 0.093s | 0.111s | 0.118s |
| Java (median-of-three) | 0.086s | 0.090s | 0.091s | 0.093s | 0.111s | 0.130s |

## Sorted Input

| Implementation | 1 | 10 | 100 | 1,000 | 10,000 | 100,000 |
|---|---|---|---|---|---|---|
| Python (default) | 0.021s | 0.021s | 0.021s | 0.049s | 2.993s | 291.108s |
| Python (median-of-three) | 0.021s | 0.020s | 0.021s | 0.021s | 0.029s | 0.129s |
| Java (default) | 0.091s | 0.093s | 0.091s | 0.109s | 0.124s | 1.046s |
| Java (median-of-three) | 0.090s | 0.092s | 0.091s | 0.093s | 0.106s | 0.125s |

