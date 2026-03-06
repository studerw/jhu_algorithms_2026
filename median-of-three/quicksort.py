import sys
import argparse


def median_of_three_partition(A, p, r):
    k = (p + r) // 2   # midpoint index

    # Sort A[p], A[k], A[r] to find the median
    if A[p] > A[k]:
        A[p], A[k] = A[k], A[p]
    if A[p] > A[r]:
        A[p], A[r] = A[r], A[p]
    if A[k] > A[r]:
        A[k], A[r] = A[r], A[k]
    # Now A[p] <= A[k] <= A[r], so A[k] is the median — swap it into the last position
    A[k], A[r] = A[r], A[k]

    # Everything below is identical to partition()
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1


def partition(A, p, r):
    x = A[r]        # the pivot
    i = p - 1       # highest index into the low side

    for j in range(p, r):              # process each element other than the pivot
        if A[j] <= x:                  # does this element belong on the low side?
            i = i + 1                  # index of a new slot in the low side
            A[i], A[j] = A[j], A[i]   # put this element there

    A[i + 1], A[r] = A[r], A[i + 1]   # pivot goes just to the right of the low side
    return i + 1                       # new index of the pivot


def quicksort(A, p, r, partition_fn):
    if p < r:
        # Partition the subarray around the pivot using the chosen partition function
        q = partition_fn(A, p, r)
        quicksort(A, p, q - 1, partition_fn)   # recursively sort the low side
        quicksort(A, q + 1, r, partition_fn)   # recursively sort the high side


if __name__ == "__main__":
    # --- Argument parsing ---
    parser = argparse.ArgumentParser(
        description="Sort comma-separated integers using quicksort."
    )

    # Optional file input; if omitted, falls back to stdin
    parser.add_argument(
        "-f", "--file",
        metavar="FILE",
        help="path to input file containing comma-separated integers "
             "(defaults to stdin if not provided)"
    )

    # Optional partition strategy; choices are explicit so invalid values are
    # caught automatically and a helpful error is printed
    parser.add_argument(
        "-p", "--partition",
        metavar="METHOD",
        choices=["default", "median-of-three"],
        default="default",
        help="partitioning method to use: 'default' (last-element pivot) or "
             "'median-of-three' (median of first/mid/last as pivot) "
             "[default: default]"
    )

    args = parser.parse_args()

    # --- Input reading ---
    if args.file:
        # Read from the provided file path
        try:
            with open(args.file, "r") as fh:
                data = fh.read().strip()
        except OSError as e:
            print(f"Error: could not read file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Fall back to stdin (original behaviour)
        data = sys.stdin.read().strip()

    if not data:
        print("Error: no input provided.", file=sys.stderr)
        sys.exit(1)

    try:
        A = list(map(int, data.split(",")))
    except ValueError:
        print("Error: input must be comma-separated integers.", file=sys.stderr)
        sys.exit(1)

    # --- Partition function selection ---
    if args.partition == "median-of-three":
        partition_fn = median_of_three_partition
    else:
        # Covers both explicit "default" and the argparse fallback default
        partition_fn = partition

    # Quicksort uses 0-based indices: p=0, r=len-1
    quicksort(A, 0, len(A) - 1, partition_fn)

    print(",".join(map(str, A)))