# Quicksort Benchmark Results

Each cell shows wall-clock time for sorting that input with `--suppress` (output discarded).
Java was run with `-Xss64m` to provide sufficient stack space for deep recursion.

## Random Input

| Implementation | 1 | 10 | 100 | 1,000 | 10,000 | 100,000 | 1,000,000 | 10,000,000 |
|---|---|---|---|---|---|---|---|---|
| Java (default) | 0.132s | 0.134s | 0.134s | 0.140s | 0.139s | 0.153s | 0.220s | 1.033s |
| Java (median-of-three) | 0.133s | 0.133s | 0.135s | 0.134s | 0.141s | 0.153s | 0.224s | 1.021s |

## Sorted Input

| Implementation | 1 | 10 | 100 | 1,000 | 10,000 | 100,000 | 1,000,000 | 10,000,000 |
|---|---|---|---|---|---|---|---|---|
| Java (default) | 0.135s | 0.134s | 0.135s | 0.137s | 0.149s | 0.729s | 53.847s | ERROR |
| Java (median-of-three) | 0.140s | 0.133s | 0.133s | 0.135s | 0.139s | 0.150s | 0.202s | 0.788s |

