from snowflake.acl import can_view_one_on_one, can_delete_one_on_one
from snowflake.models import User, OneOnOne

user_1 = User(id='1', name="User 1")
user_2 = User(id='2', name="User 2")
user_3 = User(id='3', name="User 3")

one_on_one = OneOnOne(created_by=user_1, created_by_id='1', user=user_2, user_id='2')


def test_can_view_one_on_one_returns_true_if_created_by_user():
    assert can_view_one_on_one(one_on_one, user_1)


def test_can_view_one_on_one_returns_true_if_scheduled_with_user():
    assert can_view_one_on_one(one_on_one, user_2)


def test_can_view_one_on_one_returns_false_for_any_other_user():
    assert not can_view_one_on_one(one_on_one, user_3)


def test_can_delete_one_on_one_returns_true_if_created_by_user():
    assert can_delete_one_on_one(one_on_one, user_1)


def test_can_delete_one_on_one_returns_true_if_scheduled_with_user():
    assert can_delete_one_on_one(one_on_one, user_2)


def test_can_delete_one_on_one_returns_false_for_any_other_user():
    assert not can_delete_one_on_one(one_on_one, user_3)
