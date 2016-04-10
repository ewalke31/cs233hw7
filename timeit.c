/*
	Naively measuring the impact of caches on performance.
	You'll need an x86 Linux/UNIX system for this.

	Run this program using

		nice -20 ionice -c 2 -n 0 ./timeit >OUTPUT

	to make sure you're getting "the best possible treatment" from
	the operating system. Check out the resulting file and look at
	the patterns. (Sometimes you'll have to ignore a few outliers.)
	Then check out

		cat /proc/cpuinfo

	and see if you can find anything that would help explain the
	pattern you're seeing. (Note that depending on your machine
	the patterns may be more or less obvious. That's why I refer
	to this as a "naive" measurement.)

	Note that the optimizer should be switched off (CFLAGS=-O0) as
	it would remove some code it considers "unnecessary".
*/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 1024*1024

static int A[SIZE];

/*
	rdtsc reads a 64-bit register counting the number of cycles
	since reset. It's not accessible directly from C.
*/
static inline void
rdtsc(unsigned int *hi, unsigned int *lo)
{
	asm volatile("rdtscp" : "=d" (*hi), "=a" (*lo) : : "%ecx");
}

int main(void)
{
	unsigned int hi0, lo0, hi1, lo1;
	int t;

	/* Just a reminder of what we're reading/writing. */
	printf("sizeof(int) = %zu\n", sizeof(int));

	/* Prime the array to show we're not cheating. */
	for (int i = 0; i < SIZE; i++) {
		t = i;
		A[i] = t;
		t = A[i];
	}

	/* Now read it back and measure. */
	printf(">>> read array elements\n");
	for (int i = 0; i < SIZE; i++) {
		rdtsc(&hi0, &lo0);
		t = A[i];
		rdtsc(&hi1, &lo1);
		assert(hi1-hi0 == 0);
		printf("%08x\t%u\n", i, lo1-lo0);
	}

	/* Now write again and measure. */
	printf(">>> write array elements\n");
	for (int i = 0; i < SIZE; i++) {
		rdtsc(&hi0, &lo0);
		A[i] = i;
		rdtsc(&hi1, &lo1);
		assert(hi1-hi0 == 0);
		printf("%08x\t%u\n", i, lo1-lo0);
	}

	return EXIT_SUCCESS;
}
