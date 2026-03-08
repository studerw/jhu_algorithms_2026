import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * QuickSort — sorts comma-separated integers read from a file or stdin.
 *
 * Usage:
 *   java QuickSort [options]
 *
 * Options:
 *   -f, --file <FILE>          Input file of comma-separated integers (default: stdin)
 *   -p, --partition <METHOD>   Partition method: 'default' or 'median-of-three' (default: default)
 *   -s, --suppress             Suppress sorted output
 *   -t, --trace                Print each partition call: pivot, left count, right count.
 *                              Total call count is always printed to stderr.
 *                              WARNING: produces n-1 lines — only practical for small inputs.
 *   -h, --help                 Show this help message and exit
 */
public class QuickSort {

    /**
     * Running total of partition calls made during the sort.
     *
     * Incremented by both partition() and medianOfThreePartition() on every call.
     * The final value is always n-1 regardless of partition strategy or input order,
     * because each call places exactly one pivot in its final sorted position.
     * What differs between best and worst case is not this count but the SIZE of the
     * work done per call — visible in the --trace left/right output.
     */
    static int partitionCallCount = 0;

    // -------------------------------------------------------------------------
    // Partition: last-element pivot (Lomuto scheme)
    //
    // On sorted input this always picks the largest element as the pivot,
    // producing splits of (size-1, 0) every time — the worst case.
    // With --trace you will see right=0 on every single line.
    // -------------------------------------------------------------------------
    static int partition(int[] A, int p, int r, boolean trace) {
        int x = A[r];       // pivot: last element of the subarray
        int i = p - 1;

        for (int j = p; j < r; j++) {
            if (A[j] <= x) {
                i++;
                int tmp = A[i]; A[i] = A[j]; A[j] = tmp;
            }
        }
        int tmp = A[i + 1]; A[i + 1] = A[r]; A[r] = tmp;
        int q = i + 1;

        // Count this call and optionally trace it.
        // left  = elements to the left of the pivot  = q - p
        // right = elements to the right of the pivot = r - q
        partitionCallCount++;
        if (trace) {
            int left  = q - p;
            int right = r - q;
            int size  = r - p + 1;
            System.out.printf("[partition #%8d]  size=%8d  pivot=%10d  left=%8d  right=%8d%n",
                              partitionCallCount, size, x, left, right);
        }

        return q;
    }

    // -------------------------------------------------------------------------
    // Partition: median-of-three pivot
    //
    // On sorted input the median of first/middle/last is the middle element,
    // giving a balanced (size/2, size/2) split — O(log n) depth instead of O(n).
    // With --trace you will see roughly equal left and right values.
    // -------------------------------------------------------------------------
    static int medianOfThreePartition(int[] A, int p, int r, boolean trace) {
        int k = (p + r) / 2;  // midpoint index

        // Sort A[p], A[k], A[r] so that A[k] holds the median.
        // After these three swaps: A[p] <= A[k] <= A[r].
        if (A[p] > A[k]) { int t = A[p]; A[p] = A[k]; A[k] = t; }
        if (A[p] > A[r]) { int t = A[p]; A[p] = A[r]; A[r] = t; }
        if (A[k] > A[r]) { int t = A[k]; A[k] = A[r]; A[r] = t; }

        // Swap the median into the last position so the Lomuto logic below
        // treats it as the pivot via A[r], exactly as partition() does.
        int t = A[k]; A[k] = A[r]; A[r] = t;

        // Delegate to the standard partition now that A[r] is the median pivot.
        // Note: this increments partitionCallCount and handles tracing internally.
        return partition(A, p, r, trace);
    }

    // -------------------------------------------------------------------------
    // Recursive quicksort — mirrors the Python implementation exactly
    // -------------------------------------------------------------------------

    /**
     * Recursively sort A[p..r] in place.
     *
     * Partitions the subarray around a pivot chosen by the selected strategy,
     * then recursively sorts each half. Recursion bottoms out when p >= r.
     *
     * Worst-case time  : O(n²)       — sorted input + default partition
     * Average-case time: O(n log n)
     * Stack depth      : O(n) worst, O(log n) average
     *
     * Run with -Xss64m to provide enough stack space for worst-case depth.
     *
     * @param A                 array being sorted (modified in place)
     * @param p                 left boundary (inclusive)
     * @param r                 right boundary (inclusive)
     * @param useMedianOfThree  true = median-of-three pivot, false = last-element pivot
     * @param trace             true = print each partition call's pivot and split sizes
     */
    static void quicksort(int[] A, int p, int r, boolean useMedianOfThree, boolean trace) {
        if (p < r) {
            int q = useMedianOfThree
                    ? medianOfThreePartition(A, p, r, trace)
                    : partition(A, p, r, trace);
            quicksort(A, p, q - 1, useMedianOfThree, trace);   // recursively sort the low side
            quicksort(A, q + 1, r,  useMedianOfThree, trace);  // recursively sort the high side
        }
    }

    // -------------------------------------------------------------------------
    // Help text
    // -------------------------------------------------------------------------
    static void printHelp() {
        System.out.println("Usage: java QuickSort [options]");
        System.out.println();
        System.out.println("Sort comma-separated integers using quicksort.");
        System.out.println();
        System.out.println("Options:");
        System.out.println("  -f, --file <FILE>          Path to input file containing comma-separated");
        System.out.println("                             integers (defaults to stdin if not provided)");
        System.out.println("  -p, --partition <METHOD>   Partitioning method to use:");
        System.out.println("                               'default'         last-element pivot");
        System.out.println("                               'median-of-three' median of first/mid/last");
        System.out.println("                             [default: default]");
        System.out.println("  -s, --suppress             Suppress sorted output");
        System.out.println("  -t, --trace                Print each partition call showing pivot value");
        System.out.println("                             and left/right split sizes. Total call count");
        System.out.println("                             is always printed to stderr.");
        System.out.println("                             WARNING: produces n-1 lines of output.");
        System.out.println("                             Only practical for small inputs.");
        System.out.println("  -h, --help                 Show this help message and exit");
    }

    // -------------------------------------------------------------------------
    // main
    // -------------------------------------------------------------------------
    public static void main(String[] args) throws IOException {

        // --- Argument parsing ---
        String filePath        = null;
        String partitionMethod = "default";
        boolean suppress       = false;
        boolean trace          = false;

        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "-h":
                case "--help":
                    printHelp();
                    System.exit(0);
                    break;

                case "-s":
                case "--suppress":
                    suppress = true;
                    break;

                case "-t":
                case "--trace":
                    trace = true;
                    break;

                case "-f":
                case "--file":
                    if (i + 1 >= args.length) {
                        System.err.println("Error: " + args[i] + " requires a FILE argument.");
                        System.exit(1);
                    }
                    filePath = args[++i];
                    break;

                case "-p":
                case "--partition":
                    if (i + 1 >= args.length) {
                        System.err.println("Error: " + args[i] + " requires a METHOD argument.");
                        System.exit(1);
                    }
                    partitionMethod = args[++i];
                    if (!partitionMethod.equals("default") &&
                        !partitionMethod.equals("median-of-three")) {
                        System.err.println("Error: invalid partition method '" + partitionMethod + "'.");
                        System.err.println("       Choose 'default' or 'median-of-three'.");
                        System.exit(1);
                    }
                    break;

                default:
                    System.err.println("Error: unknown argument '" + args[i] + "'.");
                    System.err.println("       Run with -h or --help for usage.");
                    System.exit(1);
            }
        }

        // --- Input reading ---
        String data;
        if (filePath != null) {
            try {
                data = Files.readString(Path.of(filePath)).strip();
            } catch (IOException e) {
                System.err.println("Error: could not read file '" + filePath + "': " + e.getMessage());
                System.exit(1);
                return;
            }
        } else {
            data = new String(System.in.readAllBytes()).strip();
        }

        if (data.isEmpty()) {
            System.err.println("Error: no input provided.");
            System.exit(1);
            return;
        }

        // --- Parse integers ---
        int[] A;
        try {
            String[] tokens = data.split(",");
            A = new int[tokens.length];
            for (int i = 0; i < tokens.length; i++) {
                A[i] = Integer.parseInt(tokens[i].strip());
            }
        } catch (NumberFormatException e) {
            System.err.println("Error: input must be comma-separated integers.");
            System.exit(1);
            return;
        }

        int n = A.length;

        // --- Sort ---
        boolean useMedianOfThree = partitionMethod.equals("median-of-three");
        quicksort(A, 0, n - 1, useMedianOfThree, trace);

        // Always print total partition call count to stderr so it is visible
        // even when --suppress is used and stdout is clean.
        System.err.printf("%n[total partition calls: %d  (n=%d,  expected n-1=%d)]%n",
                          partitionCallCount, n, n - 1);

        // --- Output ---
        if (!suppress) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < A.length; i++) {
                if (i > 0) sb.append(',');
                sb.append(A[i]);
            }
            System.out.println(sb);
        }
    }
}
