"""
Main application.
"""

# Imports
import argparse
import os.path
import sys
from config.config_reader import ConfigReader
from log.log_config import LogConfig
from log.standard_logger import StandardLogger
from log.logger import Logger
from dictionary.dictionary_config import DictionaryConfig
from dictionary.hash_dictionary_storage import HashDictionaryStorage
from dictionary.set_dictionary_storage import SetDictionaryStorage
from dictionary.dictionary import Dictionary
from input_file_provider import InputFileProvider
from scrambled_string_finder import ScrambledStringFinder


def check_arguments(args, logger: Logger) -> None:
    """
    Validates the provided command-line arguments.

    Args:
        args (Namespace): Parsed command-line arguments.
        logger (Logger): Logger for logging errors.

    Raises:
        SystemExit: If any of the provided arguments are invalid.
    """
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

def parse_arguments():
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Scrambled String Finder")
    parser.add_argument("--dictionary", required=True, help="Path to the dictionary file.")
    parser.add_argument("--input", required=True, help="Path to the input file.")
    parser.add_argument("--config", default="config.ini", help="Path to the configuration file (default: config.ini).")
    parser.add_argument("--storage", choices=["hash", "set"], default="hash",
                        help="Type of storage to use for the dictionary.")
    return parser.parse_args()

def main():
    """
    Main function to handle command-line arguments and orchestrate the program flow.
    """

    # Parse command-line arguments
    args = parse_arguments()
    config_file = args.config
    dict_file_path = args.dictionary
    input_file_path = args.input

    # Initialize configuration
    try:
        config_reader = ConfigReader(config_file)
        dict_config = config_reader.get_config("DICTIONARY", DictionaryConfig)
        log_config = config_reader.get_config("LOGGER", LogConfig)
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

    # Check command line arguments
    check_arguments(args, logger)

    try:
        # Select dictionary storage type
        storage_type = HashDictionaryStorage if args.storage == "hash" else SetDictionaryStorage
        logger.info(f"Dictionary storage type: {args.storage}")

        dictionary = Dictionary(
            storage=storage_type(),
            dictionary_config=dict_config,
            logger=logger
        )

        dictionary.load_from_file(dict_file_path)
        logger.info(f"Total length of all dictionary words: {dictionary.total_length_of_all_words}")
    except Exception as err:
        logger.error(f"Error loading dictionary: {err}")
        sys.exit(1)

    try:
        input_file_provider = InputFileProvider(input_file_path)
        input_file_provider.load()
    except Exception as err:
        logger.error(f"Error loading input file: {err}")
        sys.exit(1)

    try:
        scrambled_string_finder = ScrambledStringFinder(
            input_provider=input_file_provider,
            dictionary=dictionary,
            logger=logger
        )

        logger.always("\n\n====== Results: ")
        for case_index, count in scrambled_string_finder.find_scrambled_strings():
            logger.always(f"Case #{case_index}: {count}")
    except Exception as err:
        logger.error(f"Error finding scrambled strings: {err}")
        sys.exit(1)


# Main code of the scrambled-strings application
if __name__ == '__main__':
    main()
