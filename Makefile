.PHONY: help check-python system-deps venv install train run clean

PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
REQ := requirements.txt

help:
	@echo "make install   Create virtual environment and install packages"
	@echo "make train     Train the YOLO model"
	@echo "make run       Run the Gradio app"
	@echo "make clean     Remove virtual environment and cache files"

check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "Python is not installed."; exit 1; }

system-deps:
	sudo apt-get update
	sudo apt-get install -y libgl1 libglib2.0-0

venv: check-python
	$(PYTHON) -m venv $(VENV)

install: system-deps venv
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ)

train: install
	$(PY) train_model.py

run: install
	$(PY) code.py

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete