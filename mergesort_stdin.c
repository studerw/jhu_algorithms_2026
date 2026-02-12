#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void merge(int *arr, int *temp, int left, int mid, int right) {
    int i = left;
    int j = mid + 1;
    int k = left;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }

    while (i <= mid) {
        temp[k++] = arr[i++];
    }

    while (j <= right) {
        temp[k++] = arr[j++];
    }

    for (i = left; i <= right; i++) {
        arr[i] = temp[i];
    }
}

void merge_sort_helper(int *arr, int *temp, int left, int right) {
    if (left >= right) {
        return;
    }

    int mid = left + (right - left) / 2;
    merge_sort_helper(arr, temp, left, mid);
    merge_sort_helper(arr, temp, mid + 1, right);
    merge(arr, temp, left, mid, right);
}

void merge_sort(int *arr, int n) {
    int *temp = malloc(n * sizeof(int));
    merge_sort_helper(arr, temp, 0, n - 1);
    free(temp);
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

    merge_sort(arr, size);

//    for (int i = 0; i < size; i++) {
//        if (i > 0) printf(",");
//        printf("%d", arr[i]);
//    }
    printf("done\n");

    free(arr);
    free(line);
    return 0;
}
