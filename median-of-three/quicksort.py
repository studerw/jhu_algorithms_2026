"""
quicksort.py — Sort comma-separated integers from a file or stdin using quicksort.

Two partition strategies are available:
  - 'default'         : last-element pivot (fast in practice, but degrades to O(n²)
                        on already-sorted input, causing deep recursion)
  - 'median-of-three' : picks the median of the first, middle, and last elements as
                        the pivot, which avoids the sorted worst-case and is generally
                        more balanced

Usage:
  python quicksort.py [-f FILE] [-p METHOD] [-s] [-t]

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


def median_of_three_partition(A, p, r, trace, counter):
    """
    Partition A[p..r] using the median of A[p], A[midpoint], and A[r] as the pivot.

    Choosing the median of three elements rather than always using the last element
    avoids the worst-case O(n²) behaviour that occurs when the input is already
    sorted (or reverse-sorted). On a sorted array the last-element pivot always
    produces maximally unbalanced partitions (one side empty, one side n-1 elements),
    leading to O(n) recursion depth. The median-of-three pivot tends to split the
    array much more evenly, keeping recursion depth closer to O(log n).

    Args:
        A:       list of integers being sorted (modified in place)
        p:       left boundary index (inclusive)
        r:       right boundary index (inclusive), where the pivot will be placed
        trace:   if True, print pivot and partition sizes for each call
        counter: a one-element list [n] used to count total partition calls
                 (a list is used so the integer is mutable across recursive calls)

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
    q = i + 1

    # Count this partition call and optionally trace it.
    # left  = number of elements to the left of the pivot  = q - p
    # right = number of elements to the right of the pivot = r - q
    # A perfectly balanced split has left ≈ right ≈ size/2.
    counter[0] += 1
    if trace:
        left  = q - p
        right = r - q
        size  = r - p + 1
        print(f"[partition #{counter[0]:>8}]  size={size:>8}  pivot={x:>10}  left={left:>8}  right={right:>8}")

    return q


def partition(A, p, r, trace, counter):
    """
    Partition A[p..r] in place around the last element A[r] as the pivot.

    Rearranges the subarray so that every element to the left of the returned
    index is <= the pivot and every element to the right is > the pivot.
    The pivot ends up in its final sorted position.

    This is the standard Lomuto partition scheme. It is simple but has O(n²)
    worst-case performance when the input is already sorted, because the pivot
    is always the largest (or smallest) element, producing maximally unbalanced
    partitions and O(n) recursion depth.

    With --trace on a sorted input you will see left=size-1, right=0 on every
    single call, visually demonstrating why this degrades to O(n²).

    Args:
        A:       list of integers being sorted (modified in place)
        p:       left boundary index (inclusive)
        r:       right boundary index (inclusive); A[r] is used as the pivot
        trace:   if True, print pivot and partition sizes for each call
        counter: a one-element list [n] used to count total partition calls

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
    q = i + 1

    # Count this partition call and optionally trace it.
    # On sorted input with this partition function, x will always be the largest
    # element in the subarray, so right will always be 0 — a maximally unbalanced
    # split that forces O(n) recursive calls instead of O(log n).
    counter[0] += 1
    if trace:
        left  = q - p
        right = r - q
        size  = r - p + 1
        print(f"[partition #{counter[0]:>8}]  size={size:>8}  pivot={x:>10}  left={left:>8}  right={right:>8}")

    return q


def quicksort(A, p, r, partition_fn, trace, counter):
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
        trace:        if True, each partition call prints its pivot and split sizes
        counter:      one-element list [n] tracking total partition calls made
    """
    if p < r:
        q = partition_fn(A, p, r, trace, counter)
        quicksort(A, p, q - 1, partition_fn, trace, counter)   # recursively sort the low side
        quicksort(A, q + 1, r,  partition_fn, trace, counter)  # recursively sort the high side


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

    parser.add_argument(
        "-f", "--file",
        metavar="FILE",
        help="path to input file containing comma-separated integers "
             "(defaults to stdin if not provided)"
    )

    parser.add_argument(
        "-p", "--partition",
        metavar="METHOD",
        choices=["default", "median-of-three"],
        default="default",
        help="partitioning method to use: 'default' (last-element pivot) or "
             "'median-of-three' (median of first/mid/last as pivot) "
             "[default: default]"
    )

    parser.add_argument(
        "-s", "--suppress",
        action="store_true",
        help="suppress sorted output (useful for benchmarking)"
    )

    # Trace flag — prints each partition call's pivot and left/right split sizes.
    # The total call count is always printed to stderr regardless of this flag.
    # WARNING: produces n-1 lines of output — only practical for small inputs.
    # For large n, omit --trace and just observe the total call count instead.
    parser.add_argument(
        "-t", "--trace",
        action="store_true",
        help="print each partition call showing pivot value and left/right split sizes. "
             "Total call count is always printed to stderr. "
             "WARNING: produces n-1 lines — only practical for small inputs."
    )

    args = parser.parse_args()

    # --- Input reading ---
    if args.file:
        try:
            with open(args.file, "r") as fh:
                data = fh.read().strip()
        except OSError as e:
            print(f"Error: could not read file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        data = sys.stdin.read().strip()

    if not data:
        print("Error: no input provided.", file=sys.stderr)
        sys.exit(1)

    try:
        A = list(map(int, data.split(",")))
    except ValueError:
        print("Error: input must be comma-separated integers.", file=sys.stderr)
        sys.exit(1)

    n = len(A)

    # --- Partition function selection ---
    if args.partition == "median-of-three":
        partition_fn = median_of_three_partition
    else:
        partition_fn = partition

    # counter is a one-element list so it can be mutated inside recursive calls.
    # Every call to partition() or median_of_three_partition() increments counter[0]
    # by 1. The total will always be n-1 (each call places exactly one pivot in its
    # final position). What differs between best and worst case is not the call count
    # but the SIZE of the work done per call — visible in the --trace left/right output.
    counter = [0]

    quicksort(A, 0, n - 1, partition_fn, args.trace, counter)

    # Always print the total partition call count to stderr so it is visible
    # even when --suppress is used and stdout is clean.
    print(f"\n[total partition calls: {counter[0]}  (n={n},  expected n-1={n-1})]", file=sys.stderr)

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
