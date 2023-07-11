#!/bin/bash

set -e

# Default values
build=false
run=false
clean=false

# Process arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --build)
            build=true
            shift # past argument
            ;;
        --run)
            run=true
            shift # past argument
            ;;
        --clean)
            clean=true
            shift # past argument
            ;;
        *)
            echo "Unknown option $key"
            exit 1
            ;;
    esac
done

if [ "$build" = true ]; then
    # if build dir does not exist, create it
    if [ ! -d "build" ]; then
        mkdir build
    fi

    cd build
    cmake -DCMAKE_INSTALL_PREFIX=/Users/niels/Workspace/cyprometheus/cyprometheus/cpp ..
    make -j8
    make install
    cd ..
fi

if [ "$clean" = true ]; then
    # if build dir exists, remove it
    if [ -d "build" ]; then
        rm -rf build
    fi
    # if _skbuild dir exists, remove it
    if [ -d "_skbuild" ]; then
        rm -rf _skbuild
    fi

    # remove all *.so files
    find . -type f -name '*.so' -delete
    # Delete .pyc, .pyo, and __pycache__ files
    find . -type f \( -name '*.py[co]' -o -type d -name '__pycache__' \) -delete
    # Delete .o files
    find . -type f -name '*.o' -delete
    
    rm -f ./cyprometheus/foo/foo_init.cpp
fi

# Run server if requested
if [ "$run" = true ]; then
    COMMAND="python3 server.py"

    # Run the command
    eval "${COMMAND}" 
fi
