test: lint lint-tests
	pytest --cov=snowflake --cov-report=term:skip-covered tests -v

lint-tests:
	mypy tests
	pylint --disable=duplicate-code tests

lint:
	mypy snowflake
	pylint snowflake
