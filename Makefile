CODEBASE_DIR_PATH=nlp_gems

.PHONY: build
build:
	@poetry install --only main --sync

type-check:
	poetry run mypy "$(CODEBASE_DIR_PATH)"

lint: type-check
	poetry run ruff check --extend-select I "$(CODEBASE_DIR_PATH)"
	poetry run ruff format --check "$(CODEBASE_DIR_PATH)"

format:
	poetry run ruff format "$(CODEBASE_DIR_PATH)"
	poetry run ruff check --extend-select I --fix "$(CODEBASE_DIR_PATH)"

clean:
	@find . -name "__pycache__" -exec rm -rf {} \
	+ -o -name "*.pyc" -exec rm -f {} \
	+ -o -name "*.pyo" -exec rm -f {} \
	+ -o -name "*~" -exec rm -f {} +

.PHONY: test
test:
	poetry run python -m pytest -v $(PYTEST_OPTIONS)
