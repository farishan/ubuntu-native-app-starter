.PHONY: run test lint smoke install clean

PYTHON ?= python3

run:
	$(PYTHON) -m native_app

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m compileall -q src tests

smoke: lint
	PYTHONPATH=src $(PYTHON) -c "import native_app; print('import ok', native_app.__version__)"

install:
	$(PYTHON) -m pip install --user .

clean:
	rm -rf build dist *.egg-info .pytest_cache __pycache__ src/*/__pycache__ tests/__pycache__