# Based on:
# https://github.com/scikit-build/scikit-build-core/tree/main/docs/examples/getting_started/fortran

cmake_minimum_required(VERSION 3.17.2...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

# F2PY headers
execute_process(
  COMMAND "${PYTHON_EXECUTABLE}" -c
          "import numpy.f2py; print(numpy.f2py.get_include())"
  OUTPUT_VARIABLE F2PY_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE)

add_library(fortranobject OBJECT "${F2PY_INCLUDE_DIR}/fortranobject.c")
target_link_libraries(fortranobject PUBLIC Python::NumPy)
target_include_directories(fortranobject PUBLIC "${F2PY_INCLUDE_DIR}")
set_property(TARGET fortranobject PROPERTY POSITION_INDEPENDENT_CODE ON)

add_custom_command(
  OUTPUT solidmodule.c solid-f2pywrappers.f
  DEPENDS src/pysolid/solid.for
  VERBATIM
  COMMAND "${Python_EXECUTABLE}" -m numpy.f2py
          "${CMAKE_CURRENT_SOURCE_DIR}/src/pysolid/solid.for" -m solid --lower)

python_add_library(
  solid MODULE "${CMAKE_CURRENT_BINARY_DIR}/solidmodule.c"
  "${CMAKE_CURRENT_BINARY_DIR}/solid-f2pywrappers.f"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/pysolid/solid.for" WITH_SOABI)
target_link_libraries(solid PRIVATE fortranobject)

install(TARGETS solid DESTINATION pysolid)
