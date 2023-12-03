# CSP with Python

Build [CSP](https://github.com/libcsp/libcsp.git) library as a shared library and use cython bindings to script the communication with the device.

## Plan

Build libcsp v1.6 including the python bindings, and prepare a python script for it

## Requirements

The library will build under only certain conditions.

- Linux OS
- Socket CAN: `sudo apt install libsocketcan-dev`
- ZMQ: `sudo apt install libzmq3-dev`

## To build

From the `csp_python` folder:

```
> cmake . -G Ninja -B build
...
it generates the build files
...
> cd build
> ninja
...
builds the sources
```

This steps should have created both `libcsp.so` and `libcsp_py3.cpython-310-x86_64-linux-gnu.so` in the `build` folder.
