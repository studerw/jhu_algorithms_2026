import java.util.Arrays;

public class RodCuttingDP {

    /**
     * Computes the maximum revenue obtainable by cutting up a rod of length n
     * and selling the pieces according to the given price table.
     *
     * @param prices array where prices[i-1] is the price of a rod of length i
     * @param n      the length of the rod to cut
     * @return the maximum revenue obtainable
     */
    public static int cutRod(int[] prices, int n) {
        assert prices != null && prices.length > 0 : "list of prices must not be empty";
        assert n > 0 : "n must be greater than 0";

        int[] cache = new int[n + 1];
        Arrays.fill(cache, -1);
        return cutRodHelper(prices, n, cache);
    }

    /**
     * Helper function with memoization
     */
    private static int cutRodHelper(int[] prices, int n, int[] cache) {
        // base case
        if (n <= 0) {
            return 0;
        }

        // check cache
        if (cache[n] != -1) {
            return cache[n];
        }

        int max = Integer.MIN_VALUE;

        // try all possible first cuts
        for (int i = 1; i <= n; i++) {
            int price = prices[i - 1]; // price for a rod of length i
            int result = price + cutRodHelper(prices, n - i, cache);
            max = Math.max(max, result);
        }

        // store in cache
        cache[n] = max;
        return max;
    }

    public static void main(String[] args) {
        int result;

        result = cutRod(new int[]{1}, 1); // should be 1
        System.out.println("Result: " + result);
        assert result == 1 : "Expected 1, got " + result;

        result = cutRod(new int[]{1, 5}, 2); // should be 5
        System.out.println("Result: " + result);
        assert result == 5 : "Expected 5, got " + result;

        result = cutRod(new int[]{1, 5, 8}, 3); // should be 8
        System.out.println("Result: " + result);
        assert result == 8 : "Expected 8, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9}, 4); // should be 10
        System.out.println("Result: " + result);
        assert result == 10 : "Expected 10, got " + result;

        result = cutRod(new int[]{2, 5, 7, 8, 10}, 5); // should be 12
        System.out.println("Result: " + result);
        assert result == 12 : "Expected 12, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9, 10, 17}, 6); // should be 17
        System.out.println("Result: " + result);
        assert result == 17 : "Expected 17, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9, 10, 17, 17}, 7); // should be 18
        System.out.println("Result: " + result);
        assert result == 18 : "Expected 18, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9, 10, 17, 17, 20}, 8); // should be 22
        System.out.println("Result: " + result);
        assert result == 22 : "Expected 22, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9, 10, 17, 17, 20, 24}, 9); // should be 25
        System.out.println("Result: " + result);
        assert result == 25 : "Expected 25, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9, 10, 17, 17, 20, 24, 30}, 10); // should be 30
        System.out.println("Result: " + result);
        assert result == 30 : "Expected 30, got " + result;

        result = cutRod(new int[]{3, 5, 8, 9, 10, 17, 17, 20, 24, 30, 33, 36, 39, 40, 43}, 15); // should be 45
        System.out.println("Result: " + result);
        assert result == 45 : "Expected 45, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 33, 36, 39, 40, 43, 45, 49, 50, 54, 57}, 20); // should be 60
        System.out.println("Result: " + result);
        assert result == 60 : "Expected 60, got " + result;

        result = cutRod(new int[]{1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 33, 36, 39, 40, 43, 45, 49, 50, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87}, 30); // should be 90
        System.out.println("Result: " + result);
        assert result == 90 : "Expected 90, got " + result;

        result = cutRod(new int[]{3, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118, 121, 124, 127, 130, 133, 136, 139, 142, 145, 148, 151}, 50); // should be 153
        System.out.println("Result: " + result);
        assert result == 175 : "Expected 153, got " + result;

        System.out.println("\nAll tests passed!");
    }
}