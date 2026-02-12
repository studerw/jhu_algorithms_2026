## Algorithms JHU 605.621 82 - Spring 2026

Various python scripts and sub projects for Johns Hopkins Algorithms 605.621 class

### Module 3 and 4 - Testing Sorting algorithms

There are a couple versions of sorting algorithms I had AI generate
to see just how fast my own Macbook could sort large arrays e.g. up to a few million.

To generate a input file of x random integers:

```shell
python generate_random_ints_csv.py 1000000 > one_million_random_ints.txt
```

Now See how fast the various sorts can sort it.

```shell
gcc introsort_stdin.c -o introsort_stdin
gcc mergesort_stdin.c -o mergesort_stdin

time ./introsort_stdin < one_million_random_ints.txt
time ./mergesort_stdin < one_million_random_ints.txt
time python mergesort_stdin < one_million_random_ints.txt 
```

On my Macbook Air M2, the two sorts written in C only took about 300 milliseconds. 

The python version of mergesort took about 2.5 seconds.

Note that in all three source files, I've commented out the output of the sorted array because printing
a million integers to stdout greatly slows down the time it takes for the program to finish, even though 
the array has already been fully sorted. 