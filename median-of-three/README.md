# Quicksort

A command-line Python implementation of quicksort with two selectable partitioning strategies.

## Features

- Sorts comma-separated integers via **stdin** or a **file**
- Two partition strategies: standard last-element pivot, or median-of-three pivot
- Clean error handling for bad input and missing files

## Requirements

- Python 3.x (no third-party dependencies)

## Usage

```
python quicksort.py [-f FILE] [-p METHOD]
```

### Options

| Flag | Long form | Values | Default | Description |
|------|-----------|--------|---------|-------------|
| `-f` | `--file` | any file path | *(stdin)* | Read input from a file instead of stdin |
| `-p` | `--partition` | `default`, `median-of-three` | `default` | Partitioning strategy to use |

### Input format

Input must be a comma-separated list of integers with no spaces, either piped via stdin or stored in a file:

```
5,3,8,1,9,2
```

## Examples

**Pipe from stdin (default partition):**
```bash
echo "5,3,8,1,9,2" | python quicksort.py
# Output: 1,2,3,5,8,9
```

**Read from a file:**
```bash
python quicksort.py -f numbers.txt
```

**Use median-of-three partitioning:**
```bash
python quicksort.py -f numbers.txt -p median-of-three
```

**Stdin with median-of-three:**
```bash
echo "5,3,8,1,9,2" | python quicksort.py -p median-of-three
```

## Partition Strategies

**`default`** — Uses the last element of the subarray as the pivot. Simple and fast in the average case, but degrades to O(n²) on already-sorted or reverse-sorted input.

**`median-of-three`** — Selects the median of the first, middle, and last elements of the subarray as the pivot. Reduces the likelihood of worst-case performance on sorted or nearly-sorted input, making it a more robust choice in practice.

## Error handling

The program exits with a non-zero status and prints a message to stderr if:
- No input is provided
- Input contains non-integer or incorrectly formatted values
- A file path is given with `-f` but cannot be opened
