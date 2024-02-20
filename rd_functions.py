import ctypes
import platform
import platform

# Check the operating system
if platform.system() == 'Linux':
    # Code to execute on Linux
    rd_functions = ctypes.CDLL('./rd_functions.so')  # Replace with the actual path to your rd_functions.dll
    print("Running on Linux")
elif platform.system() == 'Windows':
    # Code to execute on Windows
    rd_functions = ctypes.CDLL('./rd_functions.dll')  # Replace with the actual path to your rd_functions.dll
    print("Running on Windows")
else:
    # Code to execute on other operating systems
    print("Running on unsupported OS: " +platform.system())
    raise("Running on unsupported OS: " +platform.system())

# Load the shared library


# Define the argument and return types for the functions

rd_functions.rdrand16_retry.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint16)]
rd_functions.rdrand16_retry.restype = ctypes.c_int

rd_functions.rdrand32_retry.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint32)]
rd_functions.rdrand32_retry.restype = ctypes.c_int

rd_functions.rdrand64_retry.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint64)]
rd_functions.rdrand64_retry.restype = ctypes.c_int

rd_functions.rdrand_get_n_uints.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
rd_functions.rdrand_get_n_uints.restype = ctypes.c_int

rd_functions.rdrand_get_bytes.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_ubyte)]
rd_functions.rdrand_get_bytes.restype = ctypes.c_int

# Call the functions
def call_rdrand16_retry(retries):
    rand_num = ctypes.c_uint16()
    success = rd_functions.rdrand16_retry(retries, ctypes.byref(rand_num))
    if success:
        print("16 bit Random number generated:", rand_num.value)
    else:
        print("16bit Error generating random number")

def call_rdrand32_retry(retries):
    rand_num = ctypes.c_uint32()
    success = rd_functions.rdrand32_retry(retries, ctypes.byref(rand_num))
    if success:
        print("32 bit Random number generated:", rand_num.value)
    else:
        print("32 bit Error generating random number")

def call_rdrand64_retry(retries):
    rand_num = ctypes.c_uint64()
    success = rd_functions.rdrand64_retry(retries, ctypes.byref(rand_num))
    if success:
        print("64 bit Random number generated:", rand_num.value)
    else:
        print("64 bit Error generating random number")

def call_rdrand_get_n_uints(length):
    dest = (ctypes.c_uint * length)()  # Create an array of unsigned ints
    result = rd_functions.rdrand_get_n_uints(length, dest)
    if result == length:
        print("Generated all requested random ints")
    else:
        print("Failed to generate all requested random ints. ")
    print("Random ints of length: {0} generated: {1}".format (len(dest), ",".join(map(str,dest))))
def call_rdrand_get_bytes(length):
    dest = (ctypes.c_ubyte * length)()  # Create an array of bytes
    result = rd_functions.rdrand_get_bytes(length, dest)
    obytes = bytes(dest)
    if result == length:
        print("Generated all requested random bytes")
    else:
        print("Failed to generate all requested random bytes")
    print("Random bytes {0} of length: {1} generated: {2}".format (result, len(dest), obytes ))
    for byte in obytes:
        print("{0}, bit length: {1}".format(byte, byte.bit_length()))

# Call the functions

call_rdrand16_retry(3)
call_rdrand32_retry(3)
call_rdrand64_retry(3)
call_rdrand_get_n_uints(9)
call_rdrand_get_bytes(10)

# byte_array = bytes([65, 66, 67, 68])
# print(byte_array)
# int_value = int.from_bytes(byte_array, byteorder='big')
# print(int_value)