.PHONY: help check-python venv install download-data run clean

PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
DAGSHUB := $(VENV)/bin/dagshub

REPO := svipanpreet709/3835
REMOTE_DATA := data/eggs_dataset
LOCAL_DATA := ./data
APP := code.py
REQ := requirements.txt

help:
	@echo "Available commands:"
	@echo "  make venv           Create virtual environment"
	@echo "  make install        Create venv and install dependencies"
	@echo "  make download-data  Download dataset from DagsHub bucket"
	@echo "  make run            Run the app"
	@echo "  make clean          Remove venv and cache files"

check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "Python is not installed."; exit 1; }

venv: check-python
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ)

download-data: install
	mkdir -p $(LOCAL_DATA)
	$(DAGSHUB) download --bucket $(REPO) $(REMOTE_DATA) $(LOCAL_DATA)

run: install
	$(PY) $(APP)

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete