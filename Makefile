PY=python3
VENV=venv
BIN= source $(VENV)/bin/activate
PYTHON=${}/

# Make it work on windows
ifeq ($(OS), Windows_NT)
	BIN=$(VENV)\Scripts\activate
	PYTHON=${VENV}/Scripts/python
	PY=py
endif

.PHONY: venv activate clean
# Create virtual environment
venv: $(VENV)

$(VENV):
	$(PY) -m venv $(VENV)

install: venv requirements.txt
	@echo "Installing dependencies ✨"
	$(PY) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

# Run the FastAPI server
runserver: venv
	fastapi dev src/main.py

activate: venv
	$(BIN)

# Clean up virtual environment and any other generated files
clean:
	rm -rf ./$(VENV)

# Generate requirements.txt from installed packages
freeze: venv
	$(BIN) && pip freeze > requirements.txt

# Define default target
.DEFAULT_GOAL := help

# Display help message
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  venv        to create a virtual environment"
	@echo "  install     to install dependencies"
	@echo "  run         to run the FastAPI server"
	@echo "  clean       to clean up the virtual environment"