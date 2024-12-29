#!/bin/bash

echo "================= Testing config..."
python3 -m unittest discover -v -s ./config/tests/ -p "*.py"

echo "================= Testing utils..."
python3 -m unittest discover -v -s ./utils/tests/ -p "*.py"

echo "================= Testing app..."
python3 -m unittest discover -v -s ./tests -p "*.py"
