.PHONY: test lint

test:
	pytest --cov utils_plus

lint:
	ruff check . --fix
	mypy utils_plus
