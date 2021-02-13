test: lint lint-tests
	pytest tests -v

lint-tests:
	mypy tests
	pylint --disable=duplicate-code tests

lint:
	mypy snowflake
	pylint snowflake
