## Algorithms JHU 605.621 82 - Spring 2026

Playground for JHU Algorithms class

### Module 3 and 4 - Testing Sorting algorithms

Included are a few versions of sorting algorithms I had AI generate
to see just how fast my own Macbook could sort large arrays e.g. up to a few million integers.

* To generate a input file of x random integers:

```shell
python generate_random_ints_csv.py 1000000 > one_million_random_ints.txt
```


Compile the versions written in C:

```shell
gcc introsort_stdin.c -o introsort_stdin
gcc mergesort_stdin.c -o mergesort_stdin
```

Now see how long it takes each sorting algorithm:

```shell
time ./introsort_stdin < one_million_random_ints.txt
time ./mergesort_stdin < one_million_random_ints.txt
time python mergesort_stdin < one_million_random_ints.txt 
```

On my Macbook Air M2, the two sorts written in C only took about 300 milliseconds for 1 millions integers.

The python version of mergesort took about 2.5 seconds.

Note that in all three source files, I've commented out the printing to stdout of the sorted array, because printing
a million integers to the terminal is slow, and has nothing to do with the time it takes for the sort itself. 