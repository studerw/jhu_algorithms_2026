import java.util.Arrays;
import java.util.Scanner;

public class QuickSortStdin {

    static int medianOfThreePartition(int[] A, int p, int r) {
        int k = (p + r) / 2;   // midpoint index

        // Sort A[p], A[k], A[r] to find the median
        if (A[p] > A[k]) { int tmp = A[p]; A[p] = A[k]; A[k] = tmp; }
        if (A[p] > A[r]) { int tmp = A[p]; A[p] = A[r]; A[r] = tmp; }
        if (A[k] > A[r]) { int tmp = A[k]; A[k] = A[r]; A[r] = tmp; }
        // Now A[p] <= A[k] <= A[r], so A[k] is the median — swap it into the last position
        int tmp = A[k]; A[k] = A[r]; A[r] = tmp;

        // Everything below is identical to partition()
        int x = A[r];
        int i = p - 1;
        for (int j = p; j < r; j++) {
            if (A[j] <= x) {
                i++;
                int t = A[i]; A[i] = A[j]; A[j] = t;
            }
        }
        int t = A[i + 1]; A[i + 1] = A[r]; A[r] = t;
        return i + 1;
    }


    // Partition the subarray A[p..r] around a pivot, which ends up in A[q]
    static int partition(int[] A, int p, int r) {
        int x = A[r];       // the pivot
        int i = p - 1;      // highest index into the low side

        for (int j = p; j < r; j++) {   // process each element other than the pivot
            if (A[j] <= x) {            // does this element belong on the low side?
                i = i + 1;              // index of a new slot in the low side
                int tmp = A[i];         // swap A[i] and A[j] - put this element there
                A[i] = A[j];
                A[j] = tmp;
            }
        }

        // pivot goes just to the right of the low side
        int tmp = A[i + 1];
        A[i + 1] = A[r];
        A[r] = tmp;

        return i + 1;   // new index of the pivot
    }

    // Recursively sort A[p..r]
    static void quicksort(int[] A, int p, int r) {
        if (p < r) {
            // Partition the subarray around the pivot, which ends up in A[q]
            int q = medianOfThreePartition(A, p, r);
            quicksort(A, p, q - 1);     // recursively sort the low side
            quicksort(A, q + 1, r);     // recursively sort the high side
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        if (!scanner.hasNextLine()) {
            System.err.println("Error: no input provided.");
            System.exit(1);
        }

        String line = scanner.nextLine().trim();
        scanner.close();

        if (line.isEmpty()) {
            System.err.println("Error: no input provided.");
            System.exit(1);
        }

        // Parse comma-separated integers
        String[] tokens = line.split(",");
        int[] A = new int[tokens.length];
        try {
            for (int i = 0; i < tokens.length; i++) {
                A[i] = Integer.parseInt(tokens[i].trim());
            }
        } catch (NumberFormatException e) {
            System.err.println("Error: input must be comma-separated integers. " + e.getMessage());
            System.exit(1);
        }

        quicksort(A, 0, A.length - 1);

        // Build and print comma-separated output
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < A.length; i++) {
            if (i > 0) sb.append(",");
            sb.append(A[i]);
        }
        System.out.println(sb.toString());
    }
}