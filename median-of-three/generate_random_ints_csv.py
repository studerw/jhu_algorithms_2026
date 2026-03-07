import sys
import random
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a CSV of numbers.",
        epilog=(
            "Examples:\n"
            "  python script.py 10               # 10 random numbers\n"
            "  python script.py 10 --sorted      # 1 through 10 in order\n"
            "  python script.py 10 --reverse     # 10 down to 1\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Required positional argument: how many numbers to generate
    parser.add_argument(
        "x",
        type=int,
        nargs="?",  # Makes x optional so we can catch it and print help instead of an ugly error
        help="How many numbers to generate"
    )

    # Optional flag: output numbers sorted 1 to x
    parser.add_argument(
        "-s", "--sorted",
        action="store_true",
        help="Output numbers sorted in increasing order from 1 to x"
    )

    # Optional flag: output numbers sorted x to 1
    parser.add_argument(
        "-r", "--reverse",
        action="store_true",
        help="Output numbers sorted in decreasing order from x to 1"
    )

    args = parser.parse_args()

    # If x wasn't provided, print help and exit
    if args.x is None:
        parser.print_help()
        sys.exit(1)

    # Validate x is a positive integer
    if args.x <= 0:
        print("Error: x must be a positive integer.")
        sys.exit(1)

    # --sorted and --reverse are mutually exclusive
    if args.sorted and args.reverse:
        print("Error: --sorted and --reverse cannot be used together.")
        sys.exit(1)

    # Generate the number list based on the selected mode
    if args.sorted:
        # Sequential list from 1 up to x
        numbers = list(range(1, args.x + 1))
    elif args.reverse:
        # Sequential list from x down to 1
        numbers = list(range(args.x, 0, -1))
    else:
        # Default: x random integers between 1 and 100,000
        numbers = [random.randint(1, 100000) for _ in range(args.x)]

    print(",".join(map(str, numbers)))