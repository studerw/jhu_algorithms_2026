#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void insertion_sort(int *arr, int left, int right) {
    for (int i = left + 1; i <= right; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= left && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void heapify(int *arr, int n, int i, int offset) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[offset + left] > arr[offset + largest]) {
        largest = left;
    }

    if (right < n && arr[offset + right] > arr[offset + largest]) {
        largest = right;
    }

    if (largest != i) {
        swap(&arr[offset + i], &arr[offset + largest]);
        heapify(arr, n, largest, offset);
    }
}

void heap_sort(int *arr, int left, int right) {
    int n = right - left + 1;

    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i, left);
    }

    for (int i = n - 1; i > 0; i--) {
        swap(&arr[left], &arr[left + i]);
        heapify(arr, i, 0, left);
    }
}

int median_of_three(int *arr, int left, int right) {
    int mid = left + (right - left) / 2;

    if (arr[left] > arr[mid]) {
        swap(&arr[left], &arr[mid]);
    }
    if (arr[left] > arr[right]) {
        swap(&arr[left], &arr[right]);
    }
    if (arr[mid] > arr[right]) {
        swap(&arr[mid], &arr[right]);
    }

    return mid;
}

int partition(int *arr, int left, int right) {
    int pivot_idx = median_of_three(arr, left, right);
    swap(&arr[pivot_idx], &arr[right]);
    int pivot = arr[right];

    int i = left - 1;

    for (int j = left; j < right; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }

    swap(&arr[i + 1], &arr[right]);
    return i + 1;
}

void introsort_helper(int *arr, int left, int right, int depth_limit) {
    int size = right - left + 1;

    if (size < 16) {
        insertion_sort(arr, left, right);
        return;
    }

    if (depth_limit == 0) {
        heap_sort(arr, left, right);
        return;
    }

    int pivot = partition(arr, left, right);
    introsort_helper(arr, left, pivot - 1, depth_limit - 1);
    introsort_helper(arr, pivot + 1, right, depth_limit - 1);
}

void introsort(int *arr, int n) {
    int depth_limit = 2 * (int)log2(n);
    introsort_helper(arr, 0, n - 1, depth_limit);
}

int main() {
    char *line = NULL;
    size_t len = 0;
    getline(&line, &len, stdin);

    int capacity = 1000;
    int size = 0;
    int *arr = malloc(capacity * sizeof(int));

    char *token = strtok(line, ",");
    while (token != NULL) {
        if (size >= capacity) {
            capacity *= 2;
            arr = realloc(arr, capacity * sizeof(int));
        }
        arr[size++] = atoi(token);
        token = strtok(NULL, ",");
    }

    introsort(arr, size);

//    for (int i = 0; i < size; i++) {
//        if (i > 0) printf(",");
//        printf("%d", arr[i]);
//    }
    printf("done\n");

    free(arr);
    free(line);
    return 0;
}