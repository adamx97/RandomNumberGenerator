
#include <cstring>
#include <iostream>

extern "C"
{
// add your C #include statements here
#include "rd_functions.h"
}

void test_rdrand_get_bytes(int length)
{
    unsigned char *original_buffer = new unsigned char[length];
    unsigned char *buffer = new unsigned char[length];

    // Store the original values in original_buffer
    for (int i = 0; i < length; i++)
    {
        original_buffer[i] = buffer[i];
    }

    // unsigned char buffer[length]; // Assuming 4 bytes for the example
    unsigned int result = rdrand_get_bytes(length, buffer);

    // Compare the contents of the two buffers. it is a problem if the contents are the same after the call to rdrand_get_bytes
    int equal = 0;
    for (int i = 0; i < length; i++)
    {
        if (original_buffer[i] == buffer[i])
        {
            equal += 1;
            break;
        }
    }
    if ((length > 0) && (equal/length > 0.004))  
    // there is a very small chance that the two buffers match at any given byte, 
    // (if we zero the buffer to be all zeroes,
    // there is .0039 % chance that the contents are the same (they are both 0) because     
    // we are generating ints from 0 to 255 (1 byte). But I'm not zeroing the buffer because it is safe to use when we new it.
    {
        std::cout << "PROBLEM! Buffer is unchanged (has more than .004% matches) (Original: ";
        // Print the bytes in the original buffer
        for (int i = 0; i < length; i++)
        {
            std::cout <<  std::hex << static_cast<int>(original_buffer[i]) << " "; 
        }
        std::cout <<  ") Now: ";
    }
    else
    {
        std::cout << "GOOD: Buffer has changed ";
    }
    if (result == (unsigned int) length)
    {
        // Print the bytes in the buffer
        for (int i = 0; i < std::min(length, 20); i++)
        {
            std::cout << std::hex << static_cast<int>(buffer[i]) << " ";
        }
        std::cout << std::dec << std::endl;
    }
    else
    {
        std::cout << "Failed to generate random bytes" << std::endl;
    }
}

void test_rdrand_get_n_uints(int length)
{
    // unsigned int buffer[length];
    unsigned int *buffer = new unsigned int[length];
    unsigned int *original_buffer = new unsigned int[length];
    for (int i = 0; i < length; i++)
    {
        original_buffer[i] = buffer[i];
    }

    unsigned int result = rdrand_get_n_uints(length, buffer);

    bool equal = false;
    for (int i = 0; i < length; i++)
    {
        if (original_buffer[i] == buffer[i])
        {
            equal = true;
            break;
        }
    }
    if (equal)
    {
        std::cout << "PROBLEM! Buffer is unchanged (Original: ";
        // Print the bytes in the original buffer
        for (int i = 0; i < length; i++)
        {
            std::cout << original_buffer[i];
        }
        std::cout <<  ") Now: ";
    }
    else
    {
        std::cout << "GOOD: Buffer has changed ";
    }
    if (result == (unsigned int) length)
    {
        // Print the bytes in the buffer
        for (int i = 0; i < std::min (20,length) ; i++)
        {
            std::cout << buffer[i] << " ";
        }
        std::cout << std::endl;
    }
    else
    {
        std::cout << "Failed to generate random bytes" << std::endl;
    }
}