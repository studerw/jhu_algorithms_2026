"""
quicksort.py — Sort comma-separated integers from a file or stdin using quicksort.

Two partition strategies are available:
  - 'default'         : last-element pivot (fast in practice, but degrades to O(n²)
                        on already-sorted input, causing deep recursion)
  - 'median-of-three' : picks the median of the first, middle, and last elements as
                        the pivot, which avoids the sorted worst-case and is generally
                        more balanced

Usage:
  python quicksort.py [-f FILE] [-p METHOD] [-s]

To handle very large inputs without hitting Python's recursion limit, the program
raises sys.setrecursionlimit and runs inside a dedicated thread with a much larger
OS-level stack (64 MB). See the __main__ block at the bottom for details.
"""

import sys
import argparse
import threading

# Python's default recursion limit is only 1000 frames, which is far too shallow
# for quicksort on large inputs (worst case requires O(n) frames on sorted data).
# This raises the limit so Python itself doesn't throw a RecursionError before the
# OS stack is exhausted. The thread stack size increase below handles the OS side.
sys.setrecursionlimit(1000000)


def median_of_three_partition(A, p, r):
    """
    Partition A[p..r] using the median of A[p], A[midpoint], and A[r] as the pivot.

    Choosing the median of three elements rather than always using the last element
    avoids the worst-case O(n²) behaviour that occurs when the input is already
    sorted (or reverse-sorted). On a sorted array the last-element pivot always
    produces maximally unbalanced partitions (one side empty, one side n-1 elements),
    leading to O(n) recursion depth. The median-of-three pivot tends to split the
    array much more evenly, keeping recursion depth closer to O(log n).

    Args:
        A: list of integers being sorted (modified in place)
        p: left boundary index (inclusive)
        r: right boundary index (inclusive), where the pivot will be placed

    Returns:
        The final index of the pivot after partitioning.
    """
    k = (p + r) // 2   # index of the midpoint element

    # Sort the three candidate elements in place so that A[k] holds the median.
    # After these three conditional swaps: A[p] <= A[k] <= A[r].
    if A[p] > A[k]:
        A[p], A[k] = A[k], A[p]
    if A[p] > A[r]:
        A[p], A[r] = A[r], A[p]
    if A[k] > A[r]:
        A[k], A[r] = A[r], A[k]

    # Move the median (A[k]) to the last position so the standard partition
    # logic below can treat A[r] as the pivot, exactly as partition() does.
    A[k], A[r] = A[r], A[k]

    # From here on the logic is identical to partition(): A[r] is the pivot.
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1


def partition(A, p, r):
    """
    Partition A[p..r] in place around the last element A[r] as the pivot.

    Rearranges the subarray so that every element to the left of the returned
    index is <= the pivot and every element to the right is > the pivot.
    The pivot ends up in its final sorted position.

    This is the standard Lomuto partition scheme. It is simple but has O(n²)
    worst-case performance when the input is already sorted, because the pivot
    is always the largest (or smallest) element, producing maximally unbalanced
    partitions and O(n) recursion depth.

    Args:
        A: list of integers being sorted (modified in place)
        p: left boundary index (inclusive)
        r: right boundary index (inclusive); A[r] is used as the pivot

    Returns:
        The final index of the pivot after partitioning.
    """
    x = A[r]        # the pivot value
    i = p - 1       # i tracks the boundary of the "low side" (elements <= pivot)

    for j in range(p, r):              # scan every element except the pivot
        if A[j] <= x:                  # element belongs on the low side
            i = i + 1                  # expand the low side by one slot
            A[i], A[j] = A[j], A[i]   # move the element into that slot

    # Place the pivot immediately to the right of the low side
    A[i + 1], A[r] = A[r], A[i + 1]
    return i + 1                       # return the pivot's final position


def quicksort(A, p, r, partition_fn):
    """
    Recursively sort A[p..r] in place using the provided partition function.

    This is the standard recursive quicksort algorithm (Cormen et al., CLRS).
    It partitions the subarray around a pivot, then recursively sorts each half.
    Recursion bottoms out when the subarray has fewer than two elements (p >= r).

    Worst-case time complexity : O(n²)  — occurs on sorted input with default partition
    Average-case time complexity: O(n log n)
    Space complexity            : O(n)  worst case for the call stack (O(log n) average)

    Args:
        A:            list of integers being sorted (modified in place)
        p:            left boundary index (inclusive)
        r:            right boundary index (inclusive)
        partition_fn: callable — either partition() or median_of_three_partition()
    """
    if p < r:
        # Partition the subarray and get the pivot's final position
        q = partition_fn(A, p, r)
        quicksort(A, p, q - 1, partition_fn)   # recursively sort the low side
        quicksort(A, q +  1, r, partition_fn)  # recursively sort the high side


def main():
    """
    Entry point: parse arguments, read input, run quicksort, and print results.

    Wrapped in a function (rather than sitting directly in __main__) so that it
    can be run inside a dedicated thread with an enlarged stack — see the
    __main__ block below.
    """

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

    # Boolean flag — present means True, absent means False (no value expected)
    parser.add_argument(
        "-s", "--suppress",
        action="store_true",
        help="suppress sorted output (useful for benchmarking)"
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

    if not args.suppress:
        print(",".join(map(str, A)))


if __name__ == "__main__":
    # --- Why threading? ---
    #
    # Python's recursion limit (set above) only controls how many Python-level
    # stack frames are allowed before Python raises RecursionError. But there is
    # a second, lower-level limit: the OS thread stack size. Every function call
    # consumes some physical stack memory, and when that memory runs out the
    # process receives a hard SIGSEGV (segmentation fault) — not a catchable
    # Python exception.
    #
    # The main thread's stack size is fixed by the OS at process startup
    # (typically 1–8 MB depending on the platform) and cannot be changed after
    # the fact. However, NEW threads can be given an arbitrary stack size before
    # they are created.
    #
    # By calling threading.stack_size() BEFORE creating a thread, we tell the OS
    # to allocate a 64 MB stack for that thread. We then run all of main() — and
    # therefore all of quicksort's recursive calls — inside that thread, giving
    # the recursion far more physical stack space to work with.
    #
    # thread.join() makes the main thread wait until the worker thread finishes
    # before the process exits, so the program behaves exactly as if main() had
    # been called directly.

    threading.stack_size(64 * 1024 * 1024)  # request a 64 MB stack for new threads
    thread = threading.Thread(target=main)
    thread.start()   # launch main() in the new thread with the larger stack
    thread.join()    # wait for it to finish before exiting
