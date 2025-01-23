PY=python3
VENV=venv
BIN= source $(VENV)/bin/activate
PYTHON=${}/

# docker container run --rm -v ./src:/code/src -p 8080:80 omamori-app:dev

# Make it work on windows
ifeq ($(OS), Windows_NT)
	BIN=$(VENV)\Scripts\activate
	PYTHON=${VENV}/Scripts/python
	PY=py
endif

.PHONY: venv activate clean build lint
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

build:
	@echo "Build and start container 🐳"
	docker compose up

stopcontainer:
	@echo "Stop and remove container 🐋"
	docker compose down

createtable:
	@echo "👷Creating table in dynamodb👷"
	AWS_ACCESS_KEY_ID=X AWS_SECRET_ACCESS_KEY=X aws dynamodb create-table \
	--cli-input-json file://omamori_table_definition.json \
	--region localhost \
	--endpoint-url http://localhost:8000

# {"AttributeName": "protection_type", "KeyType": "RANGE"} needs be a sort key so It need to be unique
activate: venv
	$(BIN)

# Clean up virtual environment and any other generated files
clean:
	rm -rf ./$(VENV)

lint:
	flake8 src/.

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