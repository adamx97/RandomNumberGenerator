
// from https://www.intel.com/content/www/us/en/developer/articles/guide/intel-digital-random-number-generator-drng-software-implementation-guide.html
/*
simply pass the instruction outcome directly back to the invoking routine. A function signature for such an approach may take the form:

int rdrand(unsigned int *therand)

Here, the return value of the function acts as a flag indicating to the caller the outcome of the RDRAND instruction invocation. If the return value is 1, the variable passed by reference will be populated with a usable random value. If the return value is 0, the caller understands that the value assigned to the variable is not usable. The advantage of this approach is that it gives the caller the option to decide how to proceed based on the outcome of the call.

Code Example 3 shows this implemented for 16-, 32-, and 64-bit invocations of RDRAND using inline assembly.
*/
/* #define */

#include <stdint.h>
#include <immintrin.h>
#include <stdio.h>
#ifdef __linux__
#include <string.h>
#endif

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

// /*  implementation of RDRAND invocations with a retry loop.*/

EXPORT int rdrand16_retry(unsigned int retries, uint16_t *rand)
{
	unsigned int count = 0;

	while (count <= retries)
	{
		if (_rdrand16_step(rand))
		{
			return 1;
		}

		++count;
	}

	return 0;
}

EXPORT int rdrand32_retry(unsigned int retries, uint32_t *rand)
{
	unsigned int count = 0;

	while (count <= retries)
	{
		if (_rdrand32_step(rand))
		{
			return 1;
		}

		++count;
	}

	return 0;
}

EXPORT int rdrand64_retry(unsigned int retries, uint64_t *rand)
{
	unsigned int count = 0;
#ifdef __linux__
	unsigned long long* castrand = (unsigned long long*)rand;
#endif
#ifdef _WIN32
	uint64_t *castrand = rand;
#endif
	while (count <= retries)
	{
		if (_rdrand64_step(castrand))
		{
			return 1;
		}

		++count;
	}

	return 0;
}

// /*
// int rdrand_get_bytes(unsigned int n, unsigned char *dest)

// In this function, a data object of arbitrary size is initialized with random bytes. The size is specified by the variable n,
// and the data object is passed in as a pointer to unsigned char or void.

// Implementing this function requires a loop control structure and iterative calls to the rdrand64_step() or rdrand32_step()
// functions shown previously. To simplify, let's first consider populating an array of unsigned int with random values in this manner using rdrand32_step().
// */

// unsigned int rdrand_get_n_uints(unsigned int n, unsigned int *dest)
// {
// 	unsigned int i;
// 	uint32_t *lptr = (uint32_t *)dest;

// 	for (i = 0; i < n; ++i, ++dest)
// 	{
// 		if (!rdrand32_step(dest))
// 		{
// 			return i;
// 		}
// 	}

// 	return n;
// }

// /*
// Better:
// The function returns the number of unsigned int values assigned. The caller would check this value against the number requested
// to determine whether assignment was successful. Other implementations are possible, for example, using a retry loop to handle
// the unlikely possibility of random number unavailability.

// In the next example, we reduce the number of RDRAND calls in half by using rdrand64_step() instead of rdrand32_step().

// RDRAND_RETRIES:  It is recommended that applications attempt 10 retries in a tight loop in the unlikely event that the RDRAND instruction
// does not return a random number. This number is based on a binomial probability argument: given the design margins of the
// DRNG, the odds of ten failures in a row are astronomically small and would in fact be an indication of a larger CPU issue.

// */

int RDRAND_RETRIES = 10;

EXPORT unsigned int rdrand_get_n_uints(unsigned int n, unsigned int *dest)
{
	unsigned int i;
	uint64_t *qptr = (uint64_t *)dest;
	unsigned int total_uints = 0;
	unsigned int qwords = n / 2;

	for (i = 0; i < qwords; ++i, ++qptr)
	{
		if (rdrand64_retry(RDRAND_RETRIES, qptr))
		{
			total_uints += 2;
		}
		else
		{ // if call above fails, we will return the number of uints generated so far
			return total_uints;
		}
	}

	/* Fill the residual */

	if (n % 2)
	{
		unsigned int *uptr = (unsigned int *)qptr;

		if (_rdrand32_step(uptr))
		{
			++total_uints;
		}
	}

	return total_uints;
}

// /*
// Finally, we show how a loop control structure and rdrand64_step() can be used to populate a byte array with random values.
// */
// this code from the Intel web article cited above has a bug when n is not a multiple of 8.  It was rewritten below.
// EXPORT unsigned int rdrand_get_bytes(unsigned int n, unsigned char *dest)
// {
// 	unsigned char *headstart, *tailstart;
// 	uint64_t *blockstart;
// 	unsigned int count, ltail, lhead, lblock;
// 	uint64_t i, temprand;

// 	/* Get the address of the first 64-bit aligned block in the
// 	 * destination buffer. */

// 	headstart = dest;
// 	if (((uint64_t)headstart % (uint64_t)8) == 0)
// 	{

// 		blockstart = (uint64_t *)headstart;
// 		lblock = n;
// 		lhead = 0;
// 	}
// 	else
// 	{
// 		blockstart = (uint64_t *)(((uint64_t)headstart & ~(uint64_t)7) + (uint64_t)8);

// 		lblock = n - (8 - (unsigned int)((uint64_t)headstart & (uint64_t)8));

// 		lhead = (unsigned int)((uint64_t)blockstart - (uint64_t)headstart);
// 	}

// 	/* Compute the number of 64-bit blocks and the remaining number
// 	 * of bytes (the tail) */

// 	ltail = n - lblock - lhead;
// 	count = lblock / 8; /* The number 64-bit rands needed */

// 	if (ltail)
// 	{
// 		tailstart = (unsigned char *)((uint64_t)blockstart + (uint64_t)lblock);
// 	}

// 	/* Populate the starting, mis-aligned section (the head) */

// 	if (lhead)
// 	{
// 		if (!rdrand64_retry(RDRAND_RETRIES, &temprand))
// 		{
// 			return 0;
// 		}

// 		memcpy(headstart, &temprand, lhead);
// 	}

// 	/* Populate the central, aligned block */

// 	for (i = 0; i < count; ++i, ++blockstart)
// 	{
// 		if (!rdrand64_retry(RDRAND_RETRIES, blockstart))
// 		{
// 			return i * 8 + lhead;
// 		}
// 	}

// 	/* Populate the tail */

// 	if (ltail)
// 	{
// 		if (!rdrand64_retry(RDRAND_RETRIES, &temprand))
// 		{
// 			return count * 8 + lhead;
// 		}

// 		memcpy(tailstart, &temprand, ltail);
// 	}

// 	return n;
// }

EXPORT unsigned int rdrand_get_bytes(unsigned int n, unsigned char *dest)
{
	unsigned int total_bytes = n;
	unsigned int total_uints = n / 8;
	unsigned char *headstart = dest;
	//uint64_t *dest_uint64 = (uint64_t *)dest; BAD : consider the strict aliasing rule, which states that objects of one type cannot be accessed through a pointer of another type, except through character types (such as unsigned char *). Violating this rule can lead to undefined behavior, where the behavior of the program is unpredictable and can vary between different compilers and optimization levels.
	uint64_t temprand;
	

	// Fill complete uints first
	for (unsigned int i = 0; i < total_uints; ++i)
	{
		if (!rdrand64_retry(RDRAND_RETRIES, &temprand))
		{
			return i * 8; // Return the number of bytes generated so far
		}
		memcpy(headstart, &temprand, 8);
		headstart += 8;
		
		//dest_uint64 += 8;
	}

	// Fill the residual
	unsigned int residual_bytes = n % 8;
	if (residual_bytes > 0)
	{
		if (!rdrand64_retry(RDRAND_RETRIES, &temprand))
		{
			return total_bytes - residual_bytes; // Return the number of bytes generated so far
		}
		memcpy(headstart, &temprand, residual_bytes);
	}

	return total_bytes; // All bytes have been generated
}