import ctypes
import pathlib

__version__ = '0.0.1'

def get_libcsp() -> ctypes.CDLL:
    # Load the shared library into ctypes
    libname = pathlib.Path('libcsp/build/libcmult.so')
    return ctypes.CDLL(libname)
