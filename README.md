This project generates real random (not pseudo-random) ints or chars using the built-in RDRAND capabilities of most modern Intel and AMD processors.

This is an academic exercise demonstrating faciliity in generating C code that can be used by Python functions, then exposed via Azure web functions or AWS lambdas.  The speed seems adequate for most uses--the hardware device generates 3Gbps in the earliest stage.  Azure web function code and publicly available URLs are at: https://github.com/adamx97/randomNumberGenerator_AzureFunction

There are versions for both Linux and Windows, compilable with gcc and cl (Microsoft's Windows compiler) respectively.

More notes on this can be found in [my blog.](https://dynamicsoftwaremd.blogspot.com/2024/03/random-numbers.html)

RDRAND and RDSEED are intrinsic functions that generate random numbers based on unpredictable noise generated within the CPU itself. 

The RDRAND function is used in the rd_functions.dll.  The rd_functions.py PYTHON program demonstrates its use. The CPU_Capabilities.exe (on Windows; it is just CPU_Capabilities on Linux) program 
determines if the CPU supports the RDRAND and RDSEED functions, runs some simple tests and returns a successful exit code if the CPU supports the function.
This will be used when to determine container suitability when deploying the Lambda function in the next phase.

From the AMD documentation: 

Applications relying on random numbers are innumerable. Many high performance computing (HPC) applications including Monte Carlo simulations, 
communication protocols and gaming applications depend on random numbers. One of the ubiquitous use of unpredictable random numbers is in Cryptography. 
It underlies the security mechanism of modern communication systems such as authentication, e-commerce, etc.  The key applications of random number 
generators in the field of cryptography and internet security are: 
- Key generation operations of Cryptography 
- Authentication protocols 
- Internet Gambling 
- Encryption 
- Seeding software based pseudo-random number generators (PRNG) 
(https://www.amd.com/content/dam/amd/en/documents/pdfs/developer/aocl/amd-secure-random-number-generator-library-2.0-whitepaper.pdf)

Users of Python are seeking a drop in replacement for Python's random function are advised to use the module found at https://pypi.org/project/rdrand/0.9.0/


