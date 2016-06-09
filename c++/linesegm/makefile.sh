#!/bin/bash

# Create the build folder

mkdir -p build

# Set flags and libs used

FLAGS="-D__GXX_EXPERIMENTAL_CXX0X__ -D__cplusplus=201103L"
LIBS="-lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_imgcodecs"

# Build c++ files in the src folder

prefix="./src/"
suffix=".cpp"

SRC=$prefix"*"$suffix


for i in $SRC
do
    echo "Building file: $i"
    echo "Invoking: GCC C++ Compiler"
    file=${i#$prefix}
    file=${file%$suffix}
    CMD="g++ $FLAGS -I/usr/local/include -O0 -g3 -Wall -c -fmessage-length=0 -std=c++11 -MMD -MP -MF build/$file.d -MT build/$file.d -o build/$file.o src/$file.cpp"
    echo $CMD
    $CMD
    echo "Finished building: $i"
    echo "  "
done

# Build main file

echo "Building file: ./main.cpp"
echo "Invoking: GCC C++ Compiler"
CMD="g++ $FLAGS -I/usr/local/include -O0 -g3 -Wall -c -fmessage-length=0 -std=c++11 -MMD -MP -MF build/main.d -MT build/main.d -o build/main.o main.cpp"
echo $CMD
$CMD
echo "Finished building: ./main.cpp"
echo "  "
    
# Invoke linker

mkdir -p bin

echo "Building target: ./bin/linesegm"
echo "Invoking: GCC C++ Linker"
CMD="g++ -o ./bin/linesegm "
for i in ${SRC[@]}
do
    i=${i#$prefix}
    i=${i%$suffix}
    CMD+="build/$i.o "
done
CMD+="build/main.o  $LIBS"
echo $CMD
$CMD
echo "Finished building target: ./bin/linesegm"
echo " "

echo "Build finished"
