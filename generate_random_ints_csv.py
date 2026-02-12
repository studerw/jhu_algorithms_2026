import sys
import random

if __name__ == "__main__":
    x = int(sys.argv[1])
    numbers = [random.randint(1, 100000) for _ in range(x)]
    print(",".join(map(str, numbers)))

