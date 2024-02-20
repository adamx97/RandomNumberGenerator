This project generates real (not pseudo) random ints or chars using the built-in RDRAND capabilities of most modern Intel and AMD processors.

RDRAND and RDSEED are intrinsic functions that generate random numbers based on unpredictable noise generated within the CPU itself. 

The RDRAND function is used in the rd_functions.dll.  The rd_functions.py PYTHON program demonstrates its use. The CPU_Capabilities.exe program 
determines if the CPU supports the RDRAND and RDSEED functions and runs some simple tests.

From the AMD documentation: 

Applications relying on random numbers are innumerable. Many high performance computing (HPC) applications including Monte Carlo simulations, 
communication protocols and gaming applications depend on random numbers. One of the ubiquitous use of unpredictable random numbers is in Cryptography. 
It underlies the security mechanism of modern communication systems such as authentication, e-commerce, etc.  The key applications of random number 
generators in the field of cryptography and internet security are: 
• Key generation operations of Cryptography 
• Authentication protocols 
• Internet Gambling 
• Encryption 
• Seeding software based pseudo-random number generators (PRNG) 
(https://www.amd.com/content/dam/amd/en/documents/pdfs/developer/aocl/amd-secure-random-number-generator-library-2.0-whitepaper.pdf)

