import pytest

from snowflake.migrations import migrate


def test_migrate_raises_error_if_database_uri_is_not_defined(monkeypatch):
    monkeypatch.delenv('DATABASE_URI')

    with pytest.raises(ValueError) as exception_info:
        migrate()

    assert str(exception_info.value) == 'DATABASE_URI not defined'
