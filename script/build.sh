#!/bin/bash

while getopts i: flag
do
    case "${flag}" in
        i)
          INCLUDE=${OPTARG};;
        a)
          age=${OPTARG};;
        f)
          fullname=${OPTARG};;
    esac
done

PWD=$(pwd)
LOCATE=$(pwd)/
FILES=$(./list_py_file.py $(PWD) $(LOCATE) $(INCLUDE))

echo $INCLUDE
echo $PWD
echo $LOCATE
echo $FILES