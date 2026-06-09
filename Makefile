.PHONY: install test test-all lint upload docs

# Supported test environments as python:django pairs. Keep this explicit so
# unsupported combinations, such as Django 6 on Python < 3.12, are not run.
TEST_MATRIX ?= \
	'3.10:5.2.*' \
	'3.11:5.2.*' \
	'3.12:5.2.*' \
	'3.12:6.0.*' \
	'3.13:5.2.*' \
	'3.13:6.0.*' \
	'3.14:5.2.*' \
	'3.14:6.0.*'


install:
	uv sync --all-groups

test:
	uv run --group test pytest

test-all:
	@set -e; \
	for env in $(TEST_MATRIX); do \
		python="$${env%%:*}"; \
		django="$${env#*:}"; \
		printf '\n==> Python %s / Django %s\n' "$$python" "$$django"; \
		uv run --python "$$python" --group test --with "Django==$$django" pytest; \
	done

lint:
	uv run --group test ruff check

retest:
	uv run --group test pytest -vvv --lf

coverage:
	uv run --group test pytest --cov=django_postcode_lookup --cov-report=term-missing --cov-report=html

release:
	rm -rf dist/*
	uv build
	twine upload dist/*
