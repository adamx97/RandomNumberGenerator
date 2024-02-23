import ctypes
import platform
from timeit import timeit
import struct


class objRandomLib(object):
    _rd_functions_lib = None

    def __new__(self):
        if self._rd_functions_lib is None:
            self._rd_functions_lib = super(objRandomLib, self).__new__(self)
            # Check the operating system
            if platform.system() == "Linux":
                # Code to execute on Linux
                self._rd_functions_lib = ctypes.CDLL("./rd_functions.so")
                print("Running on Linux")
            elif platform.system() == "Windows":
                # Code to execute on Windows
                self._rd_functions_lib = ctypes.CDLL("./rd_functions.dll")
                print("Running on Windows")
            else:
                # Code to execute on other operating systems
                print("Running on unsupported OS: " + platform.system())
                raise ("Running on unsupported OS: " + platform.system())

            # Define the argument and return types for the functions
            self._rd_functions_lib.rdrand16_retry.argtypes = [
                ctypes.c_uint,
                ctypes.POINTER(ctypes.c_uint16),
            ]
            self._rd_functions_lib.rdrand16_retry.restype = ctypes.c_int

            self._rd_functions_lib.rdrand32_retry.argtypes = [
                ctypes.c_uint,
                ctypes.POINTER(ctypes.c_uint32),
            ]
            self._rd_functions_lib.rdrand32_retry.restype = ctypes.c_int

            self._rd_functions_lib.rdrand64_retry.argtypes = [
                ctypes.c_uint,
                ctypes.POINTER(ctypes.c_uint64),
            ]
            self._rd_functions_lib.rdrand64_retry.restype = ctypes.c_int

            self._rd_functions_lib.rdrand_get_n_uints.argtypes = [
                ctypes.c_uint,
                ctypes.POINTER(ctypes.c_uint),
            ]
            self._rd_functions_lib.rdrand_get_n_uints.restype = ctypes.c_int

            self._rd_functions_lib.rdrand_get_bytes.argtypes = [
                ctypes.c_uint,
                ctypes.POINTER(ctypes.c_ubyte),
            ]
            self._rd_functions_lib.rdrand_get_bytes.restype = ctypes.c_int
        return self._rd_functions_lib


class RdFunctions(object):
    def __init__(self):
        self._rd_functions_lib = objRandomLib()

    def RdRand16_Retry(self, retries):
        rand_num = ctypes.c_uint16()
        success = self._rd_functions_lib.rdrand16_retry(retries, ctypes.byref(rand_num))
        if success:
            # print("16 bit Random number generated:", rand_num.value)
            return rand_num.value
        else:
            raise ("16bit Error generating random number")

    def RdRand32_Retry(self, retries):
        rand_num = ctypes.c_uint32()
        success = self._rd_functions_lib.rdrand32_retry(retries, ctypes.byref(rand_num))
        if success:
            # print("32 bit Random number generated:", rand_num.value)
            return rand_num.value
        else:
            raise ("32 bit Error generating random number")

    def RdRand64_Retry(self, retries):
        rand_num = ctypes.c_uint64()
        success = self._rd_functions_lib.rdrand64_retry(retries, ctypes.byref(rand_num))
        if success:
            # print("64 bit Random number generated:", rand_num.value)
            return rand_num.value
        else:
            raise ("64 bit Error generating random number")

    def RdRand_Get_N_Uints(self, length):
        dest = (ctypes.c_uint * length)()  # Create an array of unsigned ints
        result = self._rd_functions_lib.rdrand_get_n_uints(length, dest)
        if result == length:
            return dest
            # print("Generated all requested random ints")
            # return ",".join(map(str, dest))
        else:
            raise ("Failed to generate all requested random ints. ")

    def RdRand_Get_Bytes(self, length):
        dest = (ctypes.c_ubyte * length)()  # Create an array of bytes
        result = self._rd_functions_lib.rdrand_get_bytes(length, dest)
        obytes = bytes(dest)
        if result == length:
            # print("Generated all requested random bytes")
            return obytes
        else:
            raise ("Failed to generate all requested random bytes")


rdObj = RdFunctions()


def add_test_set(iterable):
    for i in range(10000):
        n = rdObj.RdRand16_Retry(10)
        iterable.add(n)


def add_test_list(iterable):
    for i in range(10000):
        n = rdObj.RdRand16_Retry(10)
        iterable.append(n)


def add_test_array(iterable):
    for i in range(10000):
        n = rdObj.RdRand16_Retry(10)
        iterable.append(n)


def add_test_tuple_uints():
    n = rdObj.RdRand_Get_N_Uints(10000)
    x = tuple(n)
    # return x
    # print("Tuple contents (first 10): {0} Length: {1}").format(x[:10], len(x))


def add_test_tuple_bytes():
    n = rdObj.RdRand_Get_Bytes(10000)
    x = tuple(n)
    z = 1 + 2
    # return x
    # print("Tuple contents (first 10): {0} Length: {1}").format(x[:10], len(x))


def speedtest():
    print("Starting Speedtest")
    # results when set to 1000 iterations.  Tuple works the best as it doesn't try to determine membership when inserting the values
    # SET Execution time: 65.66611978199944 seconds
    # LIST Execution time: 59.06066305300192 seconds
    # ARRAY Execution time: 73.07742864300235 seconds
    # MULTIPLE Uints Execution time: 13.172993121999752 seconds
    mynumber = 1000
    # array seems to be the fastest. 55.1 secs vs 58.5 secs
    # execution_time = timeit(
    #     "add_test_set(iterable)",
    #     setup="from __main__ import add_test_set; iterable = set()",
    #     number=mynumber,
    # )
    # print(f"SET Execution time: {execution_time} seconds")

    # execution_time = timeit(
    #     "add_test_list(iterable)",
    #     setup="from __main__ import add_test_list; iterable = list()",
    #     number=mynumber,
    # )
    # print(f"LIST Execution time: {execution_time} seconds")

    # execution_time = timeit(
    #     "add_test_array(iterable)",
    #     setup="from __main__ import add_test_array; my_array = []; iterable = my_array",
    #     number=mynumber,
    # )
    # print(f"ARRAY Execution time: {execution_time} seconds")
    # execution_time = timeit(
    #     "add_test_tuple_uints()",
    #     setup="from __main__ import add_test_tuple_uints;",
    #     number=mynumber,
    # )
    # print(f"MULTIPLE Uints into a tuple Execution time: {execution_time} seconds")

    execution_time = timeit(
        "add_test_tuple_bytes()",
        setup="from __main__ import add_test_tuple_bytes;",
        number=mynumber,
    )
    print(f"MULTIPLE Bytes into a tuple Execution time: {execution_time} seconds")


# Call the functions
def checktuples():
    print("Checking ints tuple output")
    for i in range(0, 1000, 100):
        print("Iteration: {0}".format(i))
        n = rdObj.RdRand_Get_N_Uints(i)
        print("Uint contents (first 10): {0} Length: {1}".format(n[:10], len(n)))
        nt = tuple(n)
        print(
            "Uint tuple contents (first 10): {0} Length: {1}".format(nt[:10], len(nt))
        )
    print("Checking bytes tuple output")
    for i in range(0, 1000, 100):
        print("Iteration: {0}".format(i))
        b = rdObj.RdRand_Get_Bytes(i)
        print(r"Byte Length: {0}".format(len(b)))
        print(r"Byte contents (first 10): {0} ".format(b[:10]))
        bt = tuple(b)
        print(r"Byte tuple Length: {0}".format(len(bt)))
        print(
            r"Byte tuple contents (first 10): {0} Length: {1}".format(bt[:10], len(bt))
        )


n = rdObj.RdRand16_Retry(3)
print("Faster 16 bit: {0}".format(n))
print("Faster 32bit: {0}".format(rdObj.RdRand32_Retry(3)))
print("Faster 64bit: {0}".format(rdObj.RdRand64_Retry(3)))
n2 = rdObj.RdRand_Get_N_Uints(10)
t = ctypes.c_uint
print("On this platform, 1 uint is {0} bytes".format(ctypes.sizeof(ctypes.c_uint)))
print("Faster 10 uints: {0}".format(", ".join(map(str, n2))))
zz = rdObj.RdRand_Get_Bytes(10)
# print("Faster get bytes: {0}".format(struct.unpack(">h", zz)))
strz = [hex(x) for x in zz]
intz = [x for x in zz]
print("Faster get bytes: {0}. As hex: {1}".format(intz, " ".join(strz)))
checktuples()


speedtest()

# byte_array = bytes([65, 66, 67, 68])
# print(byte_array)
# int_value = int.from_bytes(byte_array, byteorder='big')
# print(int_value)
