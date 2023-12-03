'''
    uart.py

    utilities to define a UART devices usable by the csplib
'''

import ctypes


class UARTInterface:
    def __init__(self, com: str, baud: int):
        cfg = csp_uart_cfg_t(com=com, baudrate=baud)


# Need to define the driver data
class csp_uart_cfg_t(ctypes.Structure):
    _fields_ = [('com', ctypes.c_char_p), ('baudrate', ctypes.c_uint32)]


class csp_uart_rx_msg_t(ctypes.Structure):
    _fields_ = [('com', ctypes.c_size_t), ('baudrate', ctypes.c_uint32)]
