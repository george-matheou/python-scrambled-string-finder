.PHONY: tests install lint all

tests:
	@echo "================= Testing ================="
	chmod a+x run_tests.sh
	./run_tests.sh

install:
	@echo "======> Installing Requirements"
	@python3 -m pip install --upgrade pip
	@python3 -m pip install -r requirements.txt

lint:
	@echo "======> Linting using pylint..."
	@pylint --rcfile=pylintrc --recursive=y . || true

all: install tests lint