import sys

def parse_csv_from_stdin():
    """
    Reads a single line of comma-separated values from stdin
    and returns a list of integers.
    """
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return []
        # Split by comma, strip whitespace, and convert to int
        return [int(x.strip()) for x in input_data.split(',')]
    except ValueError:
        print("Error: Input must be a comma-separated list of integers.")
        return []

def longest_increasing_subsequence_dp(arr):
    """
    Calculates the length of the LIS using the O(n^2)
    Dynamic Programming approach.
    """
    n = len(arr)
    if n == 0:
        return 0

    # dp[i] stores the length of the LIS ending at index i
    dp = [1] * n

    # The O(n^2) nested loop approach
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

if __name__ == "__main__":
    # 1. Selection/Parsing Phase
    numbers = parse_csv_from_stdin()

    # 2. Algorithmic Phase
    if numbers:
        result = longest_increasing_subsequence_dp(numbers)
        print(f"LIS Length: {result}")
    elif not numbers and sys.stdin.isatty():
        print("No data received. usage: echo '10, 22, 9, 33' | python script.py")