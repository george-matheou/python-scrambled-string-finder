#!/bin/bash

pdoc ./config ./dictionary/ ./log/ ./tests/ \
./utils/ input_file_provider.py input_provider.py \
scrambled_string_finder.py scrambled_strings.py -o ./docs/html