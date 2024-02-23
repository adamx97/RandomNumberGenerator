cmake_minimum_required(VERSION 3.5.0)
project(CPU_Capabilities VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

add_executable(CPU_Capabilities CPU_Capabilities.cpp)
add_library(rd_functions.so SHARED rd_functions.c)
target_link_libraries(CPU_Capabilities rd_functions.so)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
