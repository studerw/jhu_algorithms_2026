import sys


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

    for j in range(p, r):          # process each element other than the pivot
        if A[j] <= x:              # does this element belong on the low side?
            i = i + 1              # index of a new slot in the low side
            A[i], A[j] = A[j], A[i]   # put this element there

    A[i + 1], A[r] = A[r], A[i + 1]   # pivot goes just to the right of the low side
    return i + 1                       # new index of the pivot

def quicksort(A, p, r):
    if p < r:
        # Partition the subarray around the pivot, which ends up in A[q]
        q = median_of_three_partition(A, p, r)
        quicksort(A, p, q - 1)     # recursively sort the low side
        quicksort(A, q + 1, r)     # recursively sort the high side

if __name__ == "__main__":
    data = sys.stdin.read().strip()

    if not data:
        print("Error: no input provided.", file=sys.stderr)
        sys.exit(1)

    try:
        A = list(map(int, data.split(",")))
    except ValueError:
        print("Error: input must be comma-separated integers.", file=sys.stderr)
        sys.exit(1)

    # Quicksort uses 0-based indices here: p=0, r=len-1
    quicksort(A, 0, len(A) - 1)

    print(",".join(map(str, A)))