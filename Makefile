.PHONY: install test upload docs


install:
	uv sync --all-extras --group test

test:
	uv run --group test pytest

retest:
	uv run --group test pytest -vvv --lf

coverage:
	uv run --group test pytest --cov=django_postcode_lookup --cov-report=term-missing --cov-report=html

docs:
	uv run --extra docs $(MAKE) -C docs html

release:
	rm -rf dist/*
	uv build
	twine upload dist/*
