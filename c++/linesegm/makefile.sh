#!/bin/bash

# Create the build folder

mkdir -p build

# Set flags and libs used

FLAGS="-D__GXX_EXPERIMENTAL_CXX0X__ -D__cplusplus=201103L"
LIBS="-lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_imgcodecs"

# Build c++ files in the src folder

SRC=("astar" "sauvola" "linelocalization" "utils")

for i in "${SRC[@]}"
do
    echo "Building file: ../src/$i.cpp"
    echo "Invoking: GCC C++ Compiler"
    CMD="g++ $FLAGS -I/usr/local/include -O0 -g3 -Wall -c -fmessage-length=0 -std=c++11 -MMD -MP -MF build/$i.d -MT build/$i.d -o build/$i.o src/$i.cpp"
    echo $CMD
    $CMD
    echo "Finished building: ../src/$i.cpp"
    echo "  "
done

# Build main file

echo "Building file: ../main.cpp"
echo "Invoking: GCC C++ Compiler"
CMD="g++ $FLAGS -I/usr/local/include -O0 -g3 -Wall -c -fmessage-length=0 -std=c++11 -MMD -MP -MF build/main.d -MT build/main.d -o build/main.o main.cpp"
echo $CMD
$CMD
echo "Finished building: ./main.cpp"
echo "  "
    
# Invoke linker

echo "Building target: linesegm"
echo "Invoking: GCC C++ Linker"
CMD="g++ -o linesegm "
for i in ${SRC[@]}
do
    CMD+="build/$i.o "
done
CMD+="build/main.o  $LIBS"
echo $CMD
$CMD
echo "Finished building target: linesegm"
echo " "

echo "Build finished"
