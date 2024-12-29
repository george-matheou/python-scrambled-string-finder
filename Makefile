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
	pylint --disable=W0107,R0903 --max-line-length=120 --recursive=y --ignore=.venv,docs .

all: tests install lint