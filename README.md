# pepperstone_code_challenge

- Fix printing of the output?
- Limits for input strings?
- Say about linting
- Say about documentation

## Missing tests
- Test inputs
- Test scrambled_string_finder
- Integration testing

## Execution

### Requirements
- Make
- python3
- Docker

### Docker
- Run the application using docker
    ```bash
        docker run --rm -it \
        -v $(pwd)/files:/app/input_files \
        -v $(pwd)/config.ini:/app/input_files/config.ini \
        scrambled-string-finder \
        --dictionary /app/input_files/dict_2.txt \
        --input /app/input_files/input_2.txt \
        --config /app/input_files/config.ini
    ```

## Future Work
- Parallel processing
- Functionality for large input files
- CI/CD