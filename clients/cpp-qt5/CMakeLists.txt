cmake_minimum_required(VERSION 2.8.11)

project(gae-progress)

set(PROGRESS_QT_INSTALL_PATH "" CACHE PATH "QT directory path." )
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} ${PROGRESS_QT_INSTALL_PATH})

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)

include_directories(".")
set(CMAKE_AUTOMOC ON)

# Find the QtWidgets library
find_package(Qt5Core)
find_package(Qt5Network)

add_executable(progress tasks.h main.cpp)
target_link_libraries(progress Qt5::Network Qt5::Core)