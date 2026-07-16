cmake_minimum_required(VERSION 3.16)
project(App)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

file(GLOB SOURCES src/*.cpp)
add_executable(app ${SOURCES})
target_include_directories(app PRIVATE include)
