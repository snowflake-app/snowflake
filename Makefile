test: lint lint-tests
	pipenv run pytest tests -v

lint-tests:
	pipenv run mypy tests
	pipenv run pylint --disable=duplicate-code tests

lint:
	pipenv run mypy snowflake
	pipenv run pylint snowflake
