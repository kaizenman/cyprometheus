cmake_minimum_required(VERSION 3.18...3.22)

project(cyprometheus)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/Cython")
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
list(APPEND CMAKE_MODULE_PATH "${Python3_SITELIB}/skbuild/resources/cmake/")
find_package(Cython REQUIRED)
find_package(PythonExtensions REQUIRED)

include(FetchContent)
FetchContent_Declare(
  prometheus_cpp
  GIT_REPOSITORY https://github.com/jupp0r/prometheus-cpp.git
  GIT_TAG        v0.12.3 # adjust this to the version you want
)
FetchContent_MakeAvailable(prometheus_cpp)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/cyprometheus/cpp)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/build/include)
include_directories(${PYTHON_INCLUDE_DIRS})

set(HEADER_FILES cyprometheus/cpp/foo/foo_setup.h)
set(SOURCE_FILES cyprometheus/cpp/foo/foo_setup.cpp)
set(FOO_CPP_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cyprometheus/foo/foo_init.cpp)
set(PYX_FILES ${CMAKE_CURRENT_SOURCE_DIR}/cyprometheus/foo/foo_init.pyx)
set(CYTHON_OUTPUT_FILES ${FOO_CPP_PATH})

add_custom_command(
    OUTPUT ${CYTHON_OUTPUT_FILES}
    COMMAND ${Python3_EXECUTABLE} -m Cython.Build.Cythonize ${PYX_FILES}
    DEPENDS ${PYX_FILES}
    COMMENT "Cythonize: ${PYX_FILES}"
)

add_custom_target(
    RunCython
    ALL
    DEPENDS ${CYTHON_OUTPUT_FILES}
)

add_library(cyprometheus)
target_sources(cyprometheus PRIVATE ${SOURCE_FILES} ${HEADER_FILES})
target_link_libraries(cyprometheus PUBLIC prometheus-cpp::core prometheus-cpp::pull)

add_library(foo_init MODULE ${FOO_CPP_PATH})
add_dependencies(foo_init RunCython)
python_extension_module(foo_init)
set_target_properties(foo_init PROPERTIES PREFIX "")
target_link_libraries(foo_init cyprometheus)

install(TARGETS cyprometheus LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX})
install(TARGETS foo_init LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/../foo/)

add_custom_target(clean_all
    COMMAND find ${CMAKE_CURRENT_SOURCE_DIR} -type f -name '*.py[co]'
    COMMAND find ${CMAKE_CURRENT_SOURCE_DIR} -type f -name '*.so'
            -delete
    COMMAND find ${CMAKE_CURRENT_SOURCE_DIR} -type f -name '*.o'
            -delete
    COMMAND ${CMAKE_COMMAND} -E remove cyprometheus/foo/foo_init.cpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Cleaning generated files"
)
