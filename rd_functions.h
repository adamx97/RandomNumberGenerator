// rd_functions.h
#include <stdint.h>

#ifndef RD_FUNCTIONS_H
#define RD_FUNCTIONS_H

#ifdef __cplusplus
extern "C"
{
#endif
    unsigned int rdrand_get_n_uints(unsigned int n, unsigned int *dest);
    unsigned int rdrand_get_bytes(unsigned int n, unsigned char *dest);
    int rdrand16_retry(unsigned int retries, uint16_t *rand);
    int rdrand32_retry(unsigned int retries, uint32_t *rand);
    int rdrand64_retry(unsigned int retries, uint64_t *rand);


    // Add other function declarations here if needed

#ifdef __cplusplus
}
#endif

#endif // RD_FUNCTIONS_H