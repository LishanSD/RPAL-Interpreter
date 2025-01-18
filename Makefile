# Makefile to run the Python script myrpal.py with command-line arguments

# Define the Python interpreter
PYTHON=python3

# Define the Python script name
SCRIPT=myrpal.py

# Default target to run the Python script with additional arguments
.PHONY: run
run:
	@$(PYTHON) $(SCRIPT) $(ARGS) || (echo Error! Please check the section 6 of the project report for the correct input format... && exit 1)

.PHONY: help
help:
	@echo "Usage:"
	@echo "  make run ARGS='data/input.txt -ast' - Run the Python script with additional arguments"
	@echo "  make help                      - Display this help message"