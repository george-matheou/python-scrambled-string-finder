#!/bin/bash

pdoc ./config ./dictionary/ ./log/ ./tests/ \
./utils/ ./input_strings/ \
scrambled_string_finder.py scrambled_strings.py -o ./docs/html