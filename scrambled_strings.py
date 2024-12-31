"""
Main application.
"""

# Imports
import argparse
import os.path
import sys
from config.config_reader import ConfigReader
from log.log_config import LogConfig
from dictionary.dictionary_config import DictionaryConfig
from config.config_utils import print_config
from log.standard_logger import StandardLogger
from dictionary.dictionary_file_provider import DictionaryFileProvider
from input_file_provider import InputFileProvider
from scrambled_string_finder import ScrambledStringFinder

def main():
    """
    Main function to handle command-line arguments and orchestrate the program flow.
    """

    # Variables
    config_file = "config.ini"

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scrambled String Finder")
    parser.add_argument("--dictionary", required=True, help="Path to the dictionary file.")
    parser.add_argument("--input", required=True, help="Path to the input file.")

    args = parser.parse_args()

    # Initialize configuration
    try:
        config_reader = ConfigReader(config_file)
        dict_config = config_reader.get_config("DICTIONARY", DictionaryConfig)
        log_config = config_reader.get_config("LOGGER", LogConfig)

        print_config("DICTIONARY", dict_config)
        print_config("LOGGER", log_config)
    except Exception as err:
        print(f"Error loading configuration: {err}")
        sys.exit(1)

    # Initialize logging
    try:
        logger = StandardLogger(log_config, "scrambled_app")
    except Exception as err:
        print(f"Error initializing logger: {err}")
        sys.exit(1)

    logger.info("Configuration and logging initialized successfully.")

    # Access and check command-line arguments
    dict_file_path = args.dictionary
    input_file_path = args.input

    if not os.path.exists(dict_file_path):
        logger.error(f"Dictionary file {dict_file_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(input_file_path):
        logger.error(f"Input file {input_file_path} does not exist.")
        sys.exit(1)

    logger.info(f"Dictionary file path: {dict_file_path}")
    logger.info(f"Input file path: {input_file_path}")

    try:
        dictionary_file_provider = DictionaryFileProvider(
            dictionary_file_path=dict_file_path,
            dictionary_config=dict_config,
        )

        dictionary_file_provider.load()
        logger.info(f"Total length of all dictionary words: {dictionary_file_provider.total_length_of_all_words}")

        print("====================")
        for key, val in dictionary_file_provider.get().items():
            print(f"{key} -> {val}")
        print("====================")
    except Exception as err:
        logger.error(f"Error loading dictionary: {err}")
        sys.exit(1)

    try:
        input_file_provider = InputFileProvider(
            input_file_path=input_file_path
        )

        input_file_provider.load()

        print("====================")
        for line in input_file_provider.get():
            print(line)
        print("====================")
    except Exception as err:
        logger.error(f"Error loading input file: {err}")
        sys.exit(1)

    try:
        scrambled_string_finder = ScrambledStringFinder(
            input_provider=input_file_provider,
            dictionary_provider=dictionary_file_provider,
        )

        results = scrambled_string_finder.find_scrambled_strings()

        # Output results
        for result in results:
            print(result)
    except Exception as err:
        logger.error(f"Error finding scrambled strings: {err}")
        sys.exit(1)


# Main code of the scrambled-strings application
if __name__ == '__main__':
    main()
