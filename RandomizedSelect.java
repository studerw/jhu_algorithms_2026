import java.util.Arrays;
import java.util.Random;

public class RandomizedSelect {

    private static Random random = new Random();

    /**
     * Finds the i-th smallest element in the array
     * @param arr The input array
     * @param p   Left index
     * @param r   Right index
     * @param i   The order statistic (1-based: 1 = smallest)
     * @return    The i-th smallest element
     */
    public static int randomizedSelect(int[] arr, int p, int r, int i) {
        // Base case: only one element
        if (p == r) {
            return arr[p];
        }

        // Partition around a random pivot
        int q = randomizedPartition(arr, p, r);

        // Number of elements in the low side plus the pivot
        int k = q - p + 1;

        if (i == k) {
            // Pivot is the answer
            return arr[q];
        } else if (i < k) {
            // Answer is in the left partition
            return randomizedSelect(arr, p, q - 1, i);
        } else {
            // Answer is in the right partition
            return randomizedSelect(arr, q + 1, r, i - k);
        }
    }

    /**
     * Partitions the array around a random pivot
     */
    private static int randomizedPartition(int[] arr, int p, int r) {
        // Choose random pivot index
        int pivotIndex = p + random.nextInt(r - p + 1);

        // Swap pivot to end
        swap(arr, pivotIndex, r);

        return partition(arr, p, r);
    }

    /**
     * Standard partition from Quicksort (Lomuto partition scheme)
     */
    private static int partition(int[] arr, int p, int r) {
        int pivot = arr[r];
        int i = p - 1;

        for (int j = p; j < r; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, r);
        return i + 1;
    }

    /**
     * Swaps two elements in the array
     */
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    /**
     * Convenience method - finds i-th smallest in array (1-based)
     */
    public static int select(int[] arr, int i) {
        if (arr == null || arr.length == 0) {
            throw new IllegalArgumentException("Array cannot be null or empty");
        }
        if (i < 1 || i > arr.length) {
            throw new IllegalArgumentException("i must be between 1 and array length");
        }

        // Make a copy to avoid modifying original array
        int[] copy = Arrays.copyOf(arr, arr.length);
        return randomizedSelect(copy, 0, copy.length - 1, i);
    }

    // ==================== MAIN METHOD FOR TESTING ====================

    public static void main(String[] args) {
        System.out.println("=== Randomized Select Tests ===\n");

        // Test 1: Simple array
        int[] arr1 = {3, 2, 9, 0, 7, 5, 4, 8, 6, 1};
        System.out.println("Test 1: " + Arrays.toString(arr1));
        System.out.println("Sorted:  " + Arrays.toString(sortedCopy(arr1)));
        System.out.println("1st smallest (min): " + select(arr1, 1));
        System.out.println("5th smallest (median): " + select(arr1, 5));
        System.out.println("10th smallest (max): " + select(arr1, 10));
        System.out.println();

        // Test 2: Array with duplicates
        int[] arr2 = {5, 3, 8, 3, 9, 1, 5, 7, 3};
        System.out.println("Test 2: " + Arrays.toString(arr2));
        System.out.println("Sorted:  " + Arrays.toString(sortedCopy(arr2)));
        System.out.println("1st smallest: " + select(arr2, 1));
        System.out.println("3rd smallest: " + select(arr2, 3));
        System.out.println("5th smallest (median): " + select(arr2, 5));
        System.out.println();

        // Test 3: Already sorted array
        int[] arr3 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        System.out.println("Test 3: " + Arrays.toString(arr3));
        System.out.println("1st smallest: " + select(arr3, 1));
        System.out.println("5th smallest: " + select(arr3, 5));
        System.out.println("10th smallest: " + select(arr3, 10));
        System.out.println();

        // Test 4: Reverse sorted array
        int[] arr4 = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
        System.out.println("Test 4: " + Arrays.toString(arr4));
        System.out.println("1st smallest: " + select(arr4, 1));
        System.out.println("5th smallest: " + select(arr4, 5));
        System.out.println("10th smallest: " + select(arr4, 10));
        System.out.println();

        // Test 5: Single element
        int[] arr5 = {42};
        System.out.println("Test 5: " + Arrays.toString(arr5));
        System.out.println("1st smallest: " + select(arr5, 1));
        System.out.println();

        // Test 6: Two elements
        int[] arr6 = {100, 50};
        System.out.println("Test 6: " + Arrays.toString(arr6));
        System.out.println("1st smallest: " + select(arr6, 1));
        System.out.println("2nd smallest: " + select(arr6, 2));
        System.out.println();

        // Test 7: Large random array - verify against sorting
        System.out.println("Test 7: Large random array verification");
        int[] arr7 = generateRandomArray(1000, 10000);
        int[] sorted7 = sortedCopy(arr7);
        boolean allPassed = true;

        for (int i = 1; i <= 10; i++) {
            int idx = i * 100; // Test 100th, 200th, ... 1000th
            int result = select(arr7, idx);
            int expected = sorted7[idx - 1];
            boolean passed = result == expected;
            allPassed &= passed;
            System.out.println("  " + idx + "th smallest: " + result +
                    " (expected: " + expected + ") " +
                    (passed ? "✓" : "✗"));
        }
        System.out.println("Large array test: " + (allPassed ? "PASSED" : "FAILED"));
        System.out.println();

        // Test 8: Negative numbers
        int[] arr8 = {-5, -10, 0, 5, -3, 8, -1};
        System.out.println("Test 8: " + Arrays.toString(arr8));
        System.out.println("Sorted:  " + Arrays.toString(sortedCopy(arr8)));
        System.out.println("1st smallest: " + select(arr8, 1));
        System.out.println("4th smallest (median): " + select(arr8, 4));
        System.out.println("7th smallest: " + select(arr8, 7));
    }

    // Helper method to get sorted copy for verification
    private static int[] sortedCopy(int[] arr) {
        int[] copy = Arrays.copyOf(arr, arr.length);
        Arrays.sort(copy);
        return copy;
    }

    // Helper method to generate random array
    private static int[] generateRandomArray(int size, int maxValue) {
        int[] arr = new int[size];
        Random rand = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = rand.nextInt(maxValue);
        }
        return arr;
    }
}