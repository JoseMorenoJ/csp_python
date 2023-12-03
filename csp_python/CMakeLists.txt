project(CSP)
cmake_minimum_required(VERSION 3.20)

set(BUILD_SHARED_LIBS ON)

add_library(csp)
set_target_properties(csp PROPERTIES C_STANDARD 11)
set_target_properties(csp PROPERTIES C_EXTENSIONS ON)
target_compile_options(csp PRIVATE -Wall -Wextra)

set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS Debug Release MinSizeRel)
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "No build type selected, default to MinSizeRel")
    set(CMAKE_BUILD_TYPE MinSizeRel CACHE STRING "Build Type" FORCE)
endif()

option(CSP_ENABLE_CSP_PRINT "Enable csp_print() function" ON)
option(CSP_PRINT_STDIO "Use vprintf() for csp_print() function" ON)

set(CSP_QFIFO_LEN 15 CACHE STRING "Length of incoming queue for router task")
set(CSP_PORT_MAX_BIND 16 CACHE STRING "Length of incoming queue for router task")
set(CSP_CONN_RXQUEUE_LEN 16 CACHE STRING "Number of packets in connection queue")
set(CSP_CONN_MAX 8 CACHE STRING "Number of new connections on socket queue")
set(CSP_BUFFER_SIZE 256 CACHE STRING "Bytes in each packet buffer")
set(CSP_BUFFER_COUNT 15 CACHE STRING "Number of total packet buffers")
set(CSP_RDP_MAX_WINDOW 5 CACHE STRING "Max window size for RDP")
set(CSP_RTABLE_SIZE 10 CACHE STRING "Number of elements in routing table")

option(CSP_LITTLE_ENDIAN "Set endianness" ON)
option(CSP_USE_RDP "Reliable Datagram Protocol" ON)
option(CSP_USE_HMAC "Hash-based message authentication code" ON)
option(CSP_USE_PROMISC "Promiscious mode" ON)
option(CSP_USE_DEDUP "Packet deduplication" ON)

option(CSP_ENABLE_PYTHON3_BINDINGS "Build Python3 binding" ON)

## Build only for linux
set(CSP_POSIX 1)

find_package(PkgConfig)

if(PKG_CONFIG_FOUND)
pkg_search_module(LIBZMQ libzmq)
if(${LIBZMQ_FOUND})
    message(STATUS "Found ${LIBZMQ_LINK_LIBRARIES} ${LIBZMQ_VERSION}")
    set(CSP_HAVE_LIBZMQ 1)
else()
    message(NOTICE "No libzmq found")
endif()

pkg_search_module(LIBSOCKETCAN libsocketcan)
if(${LIBSOCKETCAN_FOUND})
    message(STATUS "Found ${LIBSOCKETCAN_LINK_LIBRARIES} ${LIBSOCKETCAN_VERSION}")
    set(CSP_HAVE_LIBSOCKETCAN 1)
else()
    message(NOTICE "No libsocketcan found")
endif()
else()
message(NOTICE "No pkg-config found")
endif()

file(REAL_PATH libcsp/include csp_inc)
file(REAL_PATH libcsp/src csp_inc_src)
list(APPEND csp_inc ${CMAKE_CURRENT_BINARY_DIR}/include)
target_include_directories(csp
PUBLIC ${csp_inc}
PRIVATE ${csp_inc_src}
)

set(CSP_C_ARGS -Wshadow -Wcast-align -Wwrite-strings -Wno-unused-parameter)
target_compile_options(csp PRIVATE ${CSP_C_ARGS})

## add_subdirectory(src)
cmake_path(SET CSP_SRC_PATH NORMALIZE libcsp/src)

target_sources(csp PRIVATE
    ${CSP_SRC_PATH}/csp_bridge.c
    ${CSP_SRC_PATH}/csp_buffer.c
    ${CSP_SRC_PATH}/csp_conn.c
    ${CSP_SRC_PATH}/csp_crc32.c
    ${CSP_SRC_PATH}/csp_debug.c
    ${CSP_SRC_PATH}/csp_dedup.c
    ${CSP_SRC_PATH}/csp_endian.c
    ${CSP_SRC_PATH}/csp_hex_dump.c
    ${CSP_SRC_PATH}/csp_iflist.c
    ${CSP_SRC_PATH}/csp_init.c
    ${CSP_SRC_PATH}/csp_io.c
    ${CSP_SRC_PATH}/csp_port.c
    ${CSP_SRC_PATH}/csp_promisc.c
    ${CSP_SRC_PATH}/csp_qfifo.c
    ${CSP_SRC_PATH}/csp_route.c
    ${CSP_SRC_PATH}/csp_service_handler.c
    ${CSP_SRC_PATH}/csp_services.c
    ${CSP_SRC_PATH}/csp_sfp.c
    ${CSP_SRC_PATH}/rtable/csp_rtable.c
    ${CSP_SRC_PATH}/rtable/csp_rtable_static.c
    ${CSP_SRC_PATH}/transport/csp_rdp.c
    ${CSP_SRC_PATH}/transport/csp_udp.c
)

## add_subdirectory(arch)
set(CSP_POSIX 1)
## add_subdirectory(posix)
target_sources(csp PRIVATE
    ${CSP_SRC_PATH}/arch/csp_system.c
    ${CSP_SRC_PATH}/arch/csp_time.c
    ${CSP_SRC_PATH}/arch/posix/csp_clock.c
    ${CSP_SRC_PATH}/arch/posix/csp_malloc.c
    ${CSP_SRC_PATH}/arch/posix/csp_queue.c
    ${CSP_SRC_PATH}/arch/posix/csp_semaphore.c
    ${CSP_SRC_PATH}/arch/posix/csp_system.c
    ${CSP_SRC_PATH}/arch/posix/csp_thread.c
    ${CSP_SRC_PATH}/arch/posix/csp_time.c
    ${CSP_SRC_PATH}/arch/posix/pthread_queue.c
)

## add_subdirectory(crypto)
target_sources(csp PRIVATE
    ${CSP_SRC_PATH}/crypto/csp_hmac.c
    ${CSP_SRC_PATH}/crypto/csp_sha1.c
    ${CSP_SRC_PATH}/crypto/csp_xtea.c
)

## add_subdirectory(drivers)
target_sources(csp PRIVATE
    ${CSP_SRC_PATH}/drivers/usart/usart_kiss.c
    ${CSP_SRC_PATH}/drivers/usart/usart_linux.c
)

if(LIBZMQ_FOUND)
    add_library(if_zmq OBJECT ${CSP_SRC_PATH}/interfaces/csp_if_zmqhub.c)
    target_include_directories(if_zmq PRIVATE
        ${csp_inc}
        ${LIBZMQ_INCLUDE_DIRS})
    target_link_libraries(if_zmq PRIVATE ${LIBZMQ_LIBRARIES})
    target_link_libraries(csp PRIVATE if_zmq)
    if(BUILD_SHARED_LIBS)
        set_property(TARGET if_zmq PROPERTY POSITION_INDEPENDENT_CODE ON)
    endif()
else()
    # Include the zmqhub stub
    target_sources(csp PRIVATE zmqhub_mock.c)
endif()



add_library(driver_can OBJECT ${CSP_SRC_PATH}/drivers/can/can_socketcan.c)
target_include_directories(driver_can PRIVATE
    ${csp_inc}
    ${LIBSOCKETCAN_INCLUDE_DIRS})
target_link_libraries(driver_can PRIVATE
    ${LIBSOCKETCAN_LIBRARIES})
target_link_libraries(csp PRIVATE driver_can)
if(BUILD_SHARED_LIBS)
    set_property(TARGET driver_can PROPERTY POSITION_INDEPENDENT_CODE ON)
endif()

## add_subdirectory(interfaces)
target_sources(csp PRIVATE
    ${CSP_SRC_PATH}/interfaces/csp_if_can_pbuf.c
    ${CSP_SRC_PATH}/interfaces/csp_if_can.c
    ${CSP_SRC_PATH}/interfaces/csp_if_i2c.c
    ${CSP_SRC_PATH}/interfaces/csp_if_kiss.c
    ${CSP_SRC_PATH}/interfaces/csp_if_lo.c
)

if(${CSP_ENABLE_PYTHON3_BINDINGS})
    find_package(Python3 COMPONENTS Development)
    if(Python3_Development.Module_FOUND)
        Python3_add_library(libcsp_py3 MODULE WITH_SOABI ${CSP_SRC_PATH}/bindings/python/pycsp.c)
        target_include_directories(libcsp_py3 PUBLIC ${csp_inc})
        target_link_libraries(libcsp_py3 PUBLIC csp)
    else()
        message(FATAL_ERROR "Python development module not found")
    endif()
endif()

configure_file(csp_autoconfig.h.in ../libcsp/include/csp/csp_autoconfig.h)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "Zephyr")
    install(TARGETS csp LIBRARY COMPONENT runtime)
    install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/libcsp/include/;${CMAKE_CURRENT_SOURCE_DIR}/libcsp/include/;
        TYPE INCLUDE
        FILES_MATCHING PATTERN "*.h*"
)
endif()
