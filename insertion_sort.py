def insertion_sort(arr):
    # Traverse from the second element to the end
    for i in range(1, len(arr)):
        key = arr[i]

        # Move elements of arr[0..i-1] that are greater than key
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

        # Insert the key at its correct location
        arr[j + 1] = key


# Example usage:
data = [3,5,1,7,8,2,9,10,4,6]
insertion_sort(data)
print(f"Insertion Sorted array: {data}")