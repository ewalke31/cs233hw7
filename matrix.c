/*
	A simple example for impact of caches on performance.
	You'll need a Linux/UNIX system for this.

	Compile the program thusly (-O0 disables optimizations):

		gcc matrix.c -O0 -o matrix

	Measure how long it takes to run thusly:

		time ./matrix

	Measure cache performance (and branch predictions too)
	for this program thusly:

		valgrind --tool=cachegrind --branch-sim=yes ./matrix

	Then change the loop body to "matrix[j][i] = 107" instead
	and compile/measure again. You should also try and see if
	optimizations (-O1, -O2, -O3, -O4) help with any of this.
*/

#include <stdlib.h>

#define SIZE 4096

int matrix[SIZE][SIZE];

int main(void)
{
	int i, j;

	for (i = 0; i < SIZE; i++) {
		for (j = 0; j < SIZE; j++) {
			matrix[i][j] = 107;
		}
	}

	return EXIT_SUCCESS;
}
