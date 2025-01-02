#!/bin/bash

#verbose="-v"
verbose=""

echo "================= Testing config..."
python3 -m unittest discover "${verbose}" -s ./config/tests/ -p "*.py"

echo "================= Testing logging..."
python3 -m unittest discover "${verbose}" -s ./log/tests/ -p "*.py"

echo "================= Testing utils..."
python3 -m unittest discover "${verbose}" -s ./utils/tests/ -p "*.py"

echo "================= Testing dictionary..."
python3 -m unittest discover "${verbose}" -s ./dictionary/tests/ -p "*.py"

echo "================= Testing input_strings..."
python3 -m unittest discover "${verbose}" -s ./input_strings/tests/ -p "*.py"

echo "================= Testing app..."
python3 -m unittest discover "${verbose}" -s ./tests -p "*.py"
