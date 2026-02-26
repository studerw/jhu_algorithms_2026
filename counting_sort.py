def counting_sort(A, k):
    n = len(A)
    # 1. Initialize output array B and count array C
    # We use n+1 and k+1 to match the 1-based indexing in the pseudocode
    B = [0] * (n + 1)
    C = [0] * (k + 1)

    # 2. Count the occurrences of each number
    for j in range(0, n):
        C[A[j]] = C[A[j]] + 1

    # 3. Update C[i] to contain the number of elements <= i
    for i in range(1, k + 1):
        C[i] = C[i] + C[i - 1]

    # 4. Build the output array B by iterating BACKWARDS
    for j in range(n - 1, -1, -1):
        B[C[A[j]]] = A[j]
        C[A[j]] = C[A[j]] - 1

    return B[1:] # Return the sorted portion (ignoring index 0)

if __name__ == "__main__":
    # Test Case 1: Small list with duplicates
    list1 = [2, 5, 3, 0, 2, 3, 0, 3]
    k1 = 5
    result1 = counting_sort(list1, k1)
    print(f"Input 1: {list1}")
    print(f"Sorted 1: {result1}")

    # Test Case 2: Another small list
    list2 = [1, 4, 1, 2, 5, 2]
    k2 = 5
    result2 = counting_sort(list2, k2)
    print(f"\nInput 2: {list2}")
    print(f"Sorted 2: {result2}")