cmake_minimum_required(VERSION 3.6)

include(RezBuild)

set ( SRC_ROOT "src" )

file(GLOB_RECURSE py_files "${SRC_ROOT}/python/*.py")

rez_install_files(
    FILES ${py_files}
    RELATIVE ${SRC_ROOT}/python
    DESTINATION python
)

# Handle installing houdini/ files.
file(GLOB_RECURSE houdini_files RELATIVE "${CMAKE_SOURCE_DIR}" "${SRC_ROOT}/houdini/*")

rez_install_files(
    ${houdini_files}
    RELATIVE ${SRC_ROOT}/houdini
    DESTINATION houdini
)
