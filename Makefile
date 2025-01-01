.PHONY: tests install lint docs all

tests:
	@echo "======> Testing"
	@chmod +x run_tests.sh && ./run_tests.sh

install:
	@echo "======> Installing Requirements"
	@python3 -m pip install --upgrade pip
	@python3 -m pip install -r requirements.txt

lint:
	@echo "======> Linting using pylint..."
	@pylint --rcfile=pylintrc --recursive=y . || true

docs:
	@echo "======> Generating documentation..."
	@chmod +x generate_docs.sh && ./generate_docs.sh

all: install tests lint docs