def THREE_WAY_PARTITION(A):
    # 1. low_boundary = 1 (Adjusted to 0 for Python indexing)
    low_boundary = 0
    # 2. current_scanner = 1 (Adjusted to 0 for Python indexing)
    current_scanner = 0
    # 3. high_boundary = A.length (Adjusted to len(A) - 1 for Python)
    high_boundary = len(A) - 1

    # 4. while current_scanner <= high_boundary
    while current_scanner <= high_boundary:
        # 5. if A[current_scanner] == LOW (represented by 0)
            if A[current_scanner] == 0:
            # 6. swap A[low_boundary] with A[current_scanner]
            A[low_boundary], A[current_scanner] = A[current_scanner], A[low_boundary]
            # 7. low_boundary = low_boundary + 1
            low_boundary += 1
            # 8. current_scanner = current_scanner + 1
            current_scanner += 1
        # 9. else if A[current_scanner] == MID (represented by 1)
        elif A[current_scanner] == 1:
            # 10. current_scanner = current_scanner + 1
            current_scanner += 1
        # 11. else // Case for HIGH (represented by 2)
        else:
            # 12. swap A[current_scanner] with A[high_boundary]
            A[current_scanner], A[high_boundary] = A[high_boundary], A[current_scanner]
            # 13. high_boundary = high_boundary - 1
            high_boundary -= 1

    return A


# --- Test Run ---
if __name__ == "__main__":
    # Test case: Unsorted array of LOW (0), MID (1), and HIGH (2)
    test_array = [2, 0, 1, 2, 1, 0]
    print(f"Original Array: {test_array}")

    sorted_result = THREE_WAY_PARTITION(test_array)
    print(f"Sorted Array:   {sorted_result}")