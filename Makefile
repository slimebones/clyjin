export show=all
export t=.

test:
	poetry run coverage run -m pytest -x --ignore=tests/app -p no:warnings --show-capture=$(show) --failed-first $(t)

lint:
	poetry run ruff $(t)

check: lint test

coverage:
	poetry run coverage report -m

coverage.html:
	poetry run coverage html --show-contexts && python -m http.server -d htmlcov 8000

docs.serve:
	poetry run mkdocs serve -a localhost:9000 -w clyjin

docs.build:
	poetry run mkdocs build
