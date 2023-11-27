'''
    main.py

    entry point for whatever this is going to be.
'''

from csp_python import get_libcsp

if __name__ == '__main__':
    # Load the shared library into ctypes
    libcsp = get_libcsp()
