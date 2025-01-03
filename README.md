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

### Prerequisites
* Python 3.10+ (ensure that the `python3` executable is available)
  * Notes:
    * The project has been tested using Python 3.10.6 and 3.11.0.
    * It is recommended to use a virtual environment for executing the application.
* `make` (for simplified commands)
* Docker (optional)

### Install dependencies
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

### Command-Line
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

### Docker

#### Step 1: Build the Docker image
```bash
make docker_build
```

#### Step 2: Run the application using Docker
```bash
docker run --rm -it \
-v $(pwd)/examples:/app/input_files \
-v $(pwd)/config.ini:/app/input_files/config.ini \
scrambled-string-finder \
--dictionary /app/input_files/dict.txt \
--input /app/input_files/input.txt \
--config /app/input_files/config.ini
```

The above command executes the application inside a Docker container of the image named `scrambled-string-finder` that is created in Step 1. This command runs the application with the following options:
- `--rm:` Automatically removes the container when it exits.
- `-it:` Allocates a pseudo-TTY and keeps STDIN open for interactive sessions.
- `-v $(pwd)/examples:/app/input_files:` Mounts the local `examples` directory into the container at `/app/input_files` to provide input files. This enables to provide custom data (dictionary and input files) from your host machine to be processed by the application.
- `-v $(pwd)/config.ini:/app/input_files/config.ini:` Mounts the local config.ini file into the container to specify configuration settings. This allows to use your configuration settings from the host machine.

- `--dictionary, --input, --config:` Passes paths to the dictionary, input, and configuration files inside the container.

## Testing
Tests are implemented using the `unittest` framework. They cover the following:
- Configuration Management: Validates the configuration file handling and parameter validation.
- Logging: Ensures correct logging setup and behavior.
- Input Handling: Ensures input strings are read, validated, and processed correctly.
- Dictionary Operations: Tests adding, retrieving, and managing dictionary words, including scrambled word handling.
- Dictionary Storage Implementations: Tests for SetDictionaryStorage and HashDictionaryStorage.
- Scrambled String Finder: Validates the core functionality of finding scrambled and exact matches.

#### Run all tests using the following command:
```bash
make tests
```

## Linting
Code linting is an essential step to ensure code quality, maintain consistency, and follow best practices. The project uses `pylint` for linting, which provides detailed feedback on code style, errors, and potential improvements. Furthermore, linting configurations are specified in the `pylintrc` file. 

#### Linting can be performed using the following command:
```bash
make lint
```

## Documentation
The project uses the `pdoc` tool to generate detailed HTML documentation for all modules by analyzing Python code and interpreting its associated `docstrings`. This documentation includes descriptions of functions, classes, and configuration parameters, providing a comprehensive reference for developers.

The generated documentation files are exported to the `./docs/html` directory. Open the `index.html` file in a web browser to browse the complete documentation. To generate the documentation, run the following:
```bash
make docs
```

## Implementation
The application executes the following steps:
1. Parses command-line arguments using the `argparse` library.
2. Reads settings from a configuration file (`config.ini`) using the `ConfigReader` class and performs initial validations using the `pydantic` library.
3. Sets up a logging system using the provided configuration to handle both console and file logs with appropriate levels and rotation.
4. Checks the existence of the dictionary and input files to ensure they are available and accessible.
5. Initializes a `Dictionary` object, choosing between `HashDictionaryStorage` or `SetDictionaryStorage`, based on user input with `SetDictionaryStorage` as the default. Additional details on storage mechanisms are provided in `Section 2`.
6. Reads and validates words from the dictionary file and loads them into the `Dictionary` object.
7. Reads and validates strings from the input file using the `InputFileProvider` class, adhering to the constraints specified in the configuration.
8. Uses the `ScrambledStringFinder` class to match and count original or scrambled words from the dictionary in the input strings. Details on the algorithm are available in `Section 1`.
9. Outputs results for each input string in the format: `Case #x: y`, where `x` is the line number and `y` is the count of matched words.

### Section 1: Core Algorithm Description
The core algorithm is implemented in the `ScrambledStringFinder` class. It identifies dictionary words, both in their original and scrambled forms, within a given input string. The key idea is the concept of a `canonical form`. For each word, the canonical form is generated by keeping the first and last characters fixed and sorting the middle characters alphabetically. This transformation ensures scrambled and original forms of a word can be matched consistently.

#### Algorithmic Steps (pseudocode):
* For each input string `I`:
  * If `I` is empty return (Line# of `I`, Count=0)
  * Otherwise:
    * Set `Count`=0 
    * For each word `W` in the Dictionary:
      * If length(`W`) > length(`I`), skip to the next word
      * Otherwise:
        * Use a sliding window of the same length as `W` to iterate through `I`
          * For each substring `S` in `I`:
            * If the first and last characters of `S` do not match those of `W`, skip to the next substring in order to improve performance.
            * Otherwise:
              * If `S` matches `W` exactly, or the canonical form of `S` matches the canonical form of `W`, increase the counter by 1 (`Count++`) and move to the next word to prevent double counting.
    * Return (Line# of `I`, `Count`)

### Section 2: Dictionary Storage
The `Dictionary` class uses a `DictionaryDataStorage` interface (an abstract class) to manage dictionary words. This design follows the *Dependency Inversion Principle* from the *SOLID principles*, ensuring that the `Dictionary` class is not tightly coupled to any specific storage implementation. Currently, two concrete implementations of `DictionaryDataStorage` are provided: `SetDictionaryStorage` and `HashDictionaryStorage`.

#### SetDictionaryStorage
* This storage type keeps dictionary words in their original form, prioritizing storage efficiency. It is implemented using the `Set` data structure.
* Canonical forms of the words are not precomputed or stored. Instead, they are dynamically computed during comparisons. While this approach reduces memory usage, it may increase computational overhead during matching.

#### HashDictionaryStorage
* This storage type uses a hash table to store dictionary words alongside their precomputed canonical forms (as key-vale pairs).
* Precomputing and storing canonical forms facilitates efficient lookups and comparisons during scrambled word matching, prioritizing performance over storage efficiency.

#### Extensibility
* The `DictionaryDataStorage` interface provides a blueprint for creating new storage strategies. Developers can easily extend the system by implementing the required methods (`add_word`, `contains_word`, `get_all_words`, `get_canonical_word`).