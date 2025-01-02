# Scrambled String Finder

## Introduction
The Scrambled String Finder is a command-line Python application designed to count how many of the words from a dictionary appear as substrings in a long string of characters either in their original form or in their scrambled form. A valid scramble keeps the first and last letters fixed while allowing reordering of the middle characters. The scrambled or original form of the dictionary word may appear multiple times but is counted only once to determine its presence. 

The application provides the following features:
- Identify and count dictionary words and their valid scrambled forms in input strings.
- Highly configurable via an `ini` file.
- Flexible dictionary storage options (Set or Hash-based).
- Robust logging with file rotation support.
- Comprehensive unit tests to ensure reliability.
- Dockerized for ease of deployment.

## Installation

#### Prerequisites
* Python 3.10+ (ensure that the `python3` executable is available)
  * Notes:
    * The project has been tested using Python 3.10.6 and 3.11.0.
    * It is recommended to use a virtual environment for executing the application.
* `make` (for simplified commands)
* Docker (optional)

#### Install dependencies
To install the application's dependencies, simply run:
```bash
make install
```

## Configuration
The application is highly configurable via an `ini` file:
```ini
[DICTIONARY]
# Minimum length of words in the dictionary
MIN_WORD_LENGTH = 2
# Maximum length of words in the dictionary
MAX_WORD_LENGTH = 105
# Maximum total length of all dictionary words
MAX_SUM_LENGTHS_OF_ALL_WORDS = 105

[LOGGER]
# Path to the log file
LOG_FILE = /var/log/scrambled_strings/scrambled_strings.log
# Maximum size of the log file before rotation
LOG_MAX_BYTES = 10000000
# Number of rotated log files to retain
LOG_BACKUP_COUNT = 5
# Enable/disable console logging
LOG_ENABLE_CONSOLE = true
#  Logging level (CRITICAL, ERROR, WARNING, INFO and DEBUG)
LOG_LEVEL = INFO

[INPUT_STRINGS]
# Minimum length of input strings
MIN_LINE_LENGTH = 2
# Maximum length of input strings
MAX_LINE_LENGTH = 1000
```

## Usage

#### Command-Line
Run the following command from your project root directory:
```bash
python3 scrambled_strings.py --dictionary <dictionary file path> --input <dictionary file path> [--config config_file] [--storage {set,hash}]
```

Executing the application with the `--help` or `-h` command-line argument will output detailed information for the command line arguments:
```text
usage: scrambled_strings.py [-h] --dictionary DICTIONARY --input INPUT [--config CONFIG] [--storage {set,hash}]

Scrambled String Finder

options:
  -h, --help            show this help message and exit
  --dictionary DICTIONARY
                        Path to the dictionary file.
  --input INPUT         Path to the input file.
  --config CONFIG       Path to the configuration file (default: config.ini).
  --storage {set,hash}  Type of storage to use for the dictionary.
```

#### Docker
##### Step 1: Build the Docker image
```bash
make docker_build
```

##### Step 2: Run the application using docker
```bash
docker run --rm -it \
-v $(pwd)/examples:/app/input_files \
-v $(pwd)/config.ini:/app/input_files/config.ini \
scrambled-string-finder \
--dictionary /app/input_files/dict.txt \
--input /app/input_files/input.txt \
--config /app/input_files/config.ini
```

## Testing
## Linting
## Documentation
## Design Concepts
