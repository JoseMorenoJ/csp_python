'''
    main.py

    entry point for whatever this is going to be.
'''
import ctypes
import pathlib

from csp_python.interface import uart

if __name__ == '__main__':
    # Load the shared library into ctypes
    libname = pathlib.Path('csp_python/libcsp/build/libcsp.so')
    libcsp = ctypes.CDLL(libname)

    # Allocate resources
    libcsp.csp_init()

    # Initialize UART interface
    uart_if = uart.UARTInterface()

    # Free resources
    libcsp.csp_free_resources()
