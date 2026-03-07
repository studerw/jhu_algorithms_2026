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
 *   -s, --suppress             Suppress output
 *   -h, --help                 Show this help message and exit
 */
public class QuickSort {

    // -------------------------------------------------------------------------
    // Partition: last-element pivot
    // -------------------------------------------------------------------------
    static int partition(int[] A, int p, int r) {
        int x = A[r];       // pivot
        int i = p - 1;
        for (int j = p; j < r; j++) {
            if (A[j] <= x) {
                i++;
                int tmp = A[i]; A[i] = A[j]; A[j] = tmp;
            }
        }
        int tmp = A[i + 1]; A[i + 1] = A[r]; A[r] = tmp;
        return i + 1;
    }

    // -------------------------------------------------------------------------
    // Partition: median-of-three pivot
    // -------------------------------------------------------------------------
    static int medianOfThreePartition(int[] A, int p, int r) {
        int k = (p + r) / 2;  // midpoint index

        // Sort A[p], A[k], A[r] to find the median
        if (A[p] > A[k]) { int t = A[p]; A[p] = A[k]; A[k] = t; }
        if (A[p] > A[r]) { int t = A[p]; A[p] = A[r]; A[r] = t; }
        if (A[k] > A[r]) { int t = A[k]; A[k] = A[r]; A[r] = t; }
        // Now A[p] <= A[k] <= A[r], so A[k] is the median — swap to last position
        int t = A[k]; A[k] = A[r]; A[r] = t;

        // Rest is identical to partition()
        return partition(A, p, r);
    }

    // -------------------------------------------------------------------------
    // Recursive quicksort — mirrors the Python implementation exactly
    // -------------------------------------------------------------------------
    static void quicksort(int[] A, int p, int r, boolean useMedianOfThree) {
        if (p < r) {
            int q = useMedianOfThree
                    ? medianOfThreePartition(A, p, r)
                    : partition(A, p, r);
            quicksort(A, p, q - 1, useMedianOfThree);   // recursively sort the low side
            quicksort(A, q + 1, r, useMedianOfThree);   // recursively sort the high side
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
        System.out.println("  -h, --help                 Show this help message and exit");
    }

    // -------------------------------------------------------------------------
    // main
    // -------------------------------------------------------------------------
    public static void main(String[] args) throws IOException {

        // --- Argument parsing ---
        String filePath      = null;
        String partitionMethod = "default";
        boolean suppress     = false;

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

        // --- Sort ---
        boolean useMedianOfThree = partitionMethod.equals("median-of-three");
        quicksort(A, 0, A.length - 1, useMedianOfThree);

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
