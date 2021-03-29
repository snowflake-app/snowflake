SRC=$(shell find snowflake -type f -name '*.py')
TEST_SRC=$(shell find tests -type f -name '*.py')

.PHONY: all

all: snowflake tests

tests: snowflake $(TEST_SRC) .coveragerc mypy.ini pylintrc
	mypy tests
	pylint --disable=duplicate-code tests
	pytest --cov=snowflake --cov-report=term:skip-covered tests -v
	@touch tests

snowflake: $(SRC) Pipfile Pipfile.lock
	mypy snowflake
	pylint snowflake
	@touch snowflake
