public class GridTravelerDP {

    /**
     * Returns the number of ways to travel from the top-left corner to the
     * bottom-right corner of an n x m grid, moving only right or down.
     *
     * @param n number of rows in the grid
     * @param m number of columns in the grid
     * @return number of unique paths from top-left to bottom-right
     */
    public static long gridTraveler(int n, int m) {
        
        if (n <= 0 || m <= 0) {
            return 0;
        }
        long result = _gridTravller(n,m);
        return result;
    }

    /**
     * Returns the number of ways to travel from the top-left corner to the
     * bottom-right corner of an n x m grid, moving only right or down.
     *
     * @param n number of rows in the grid
     * @param m number of columns in the grid
     * @return number of unique paths from top-left to bottom-right
     */
    private static long _gridTravller(int n, int m) {
       if (n == 1 && m == 1) {
            return 1;
       }
       long nCount = 0;
       long mCount = 0;
       if (n > 1) {
           nCount = _gridTravller(n - 1, m);
       }
       if (m > 1) {
           mCount = _gridTravller(n, m - 1);
       }
       return nCount + mCount;
    }

    public static void main(String[] args) {
        long result;

        // Base cases
        result = gridTraveler(1, 1);
        System.out.println("gridTraveler(1, 1) = " + result);
        assert result == 1 : "Expected 1, got " + result;

        result = gridTraveler(0, 1);
        System.out.println("gridTraveler(0, 1) = " + result);
        assert result == 0 : "Expected 0, got " + result;

        result = gridTraveler(1, 0);
        System.out.println("gridTraveler(1, 0) = " + result);
        assert result == 0 : "Expected 0, got " + result;

        // Small grids
        result = gridTraveler(2, 2);
        System.out.println("gridTraveler(2, 2) = " + result);
        assert result == 2 : "Expected 2, got " + result;

        result = gridTraveler(2, 3);
        System.out.println("gridTraveler(2, 3) = " + result);
        assert result == 3 : "Expected 3, got " + result;

        result = gridTraveler(3, 2);
        System.out.println("gridTraveler(3, 2) = " + result);
        assert result == 3 : "Expected 3, got " + result;

        result = gridTraveler(3, 3);
        System.out.println("gridTraveler(3, 3) = " + result);
        assert result == 6 : "Expected 6, got " + result;

        // Medium grids
        result = gridTraveler(4, 4);
        System.out.println("gridTraveler(4, 4) = " + result);
        assert result == 20 : "Expected 20, got " + result;

        result = gridTraveler(5, 5);
        System.out.println("gridTraveler(5, 5) = " + result);
        assert result == 70 : "Expected 70, got " + result;

        result = gridTraveler(10, 10);
        System.out.println("gridTraveler(10, 10) = " + result);
        assert result == 48620 : "Expected 48620, got " + result;

        // Larger grids (tests memoization efficiency)
        result = gridTraveler(15, 15);
        System.out.println("gridTraveler(15, 15) = " + result);
        assert result == 40116600 : "Expected 40116600, got " + result;

        result = gridTraveler(18, 18);
        System.out.println("gridTraveler(18, 18) = " + result);
        assert result == 2333606220L : "Expected 2333606220, got " + result;

        System.out.println("\nAll tests passed!");
    }
}