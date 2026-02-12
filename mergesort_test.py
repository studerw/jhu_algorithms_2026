def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Find the middle point and divide the array
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def merge(left, right):
    sorted_arr = []
    i = j = 0

    # Compare elements from both halves and merge
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1

    # Collect remaining elements
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])

    return sorted_arr


test = [3,5,1,7,8,2,9,10,4,6]

test_merged = merge_sort(test)
print(test_merged)
