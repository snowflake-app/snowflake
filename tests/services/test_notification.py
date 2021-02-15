from unittest.mock import patch, Mock

from snowflake.models import Appreciation, Mention, User, Comment, OneOnOne, OneOnOneActionItem
from snowflake.models.notification import TYPE_COMMENT_ON_APPRECIATION_RECEIVED, \
    TYPE_COMMENT_ON_APPRECIATION_COMMENTED, TYPE_ONE_ON_ONE_SETUP, TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED
from snowflake.services.notification import notify_appreciation, notify_comment, \
    notify_one_on_one_setup, notify_one_on_one_action_item_added


@patch('snowflake.services.notification.current_user', User(id='100'))
@patch('snowflake.services.notification.db.persist')
def test_notify_appreciation_notifies_every_mentioned_user_except_current(mock_persist, app):
    with app.app_context():
        appreciation = Appreciation(id=1)
        user_1 = User(id='1')
        user_2 = User(id='2')
        appreciation.mentions = [
            Mention(id=1, user=user_1),
            Mention(id=2, user=user_2),
            Mention(id=3, user=User(id='100')),
        ]

        notify_appreciation(appreciation)

        notified_users = []
        for call in mock_persist.call_args_list:
            notification = call[0][0]
            assert notification.object_id == '1'
            notified_users.append(notification.user)

        assert notified_users == [user_1, user_2]


@patch('snowflake.services.notification.db.persist')
def test_notify_comment_notifies_users_mentions_or_commented_except_current(mock_persist: Mock,
                                                                            app):
    with app.app_context():
        current_user = User(id='100')
        user_1 = User(id='1')
        user_2 = User(id='2')
        user_3 = User(id='3')
        user_4 = User(id='4')
        appreciation = Appreciation(id=1, created_by_id='100', created_by=current_user)
        appreciation.mentions = [
            Mention(id=1, user=user_1, user_id='1'),
            Mention(id=2, user=user_2, user_id='2'),
            Mention(id=3, user=current_user, user_id='100'),
        ]
        appreciation.comments = [
            Comment(id=1, appreciation=appreciation, created_by=current_user, created_by_id='100'),
            Comment(id=2, appreciation=appreciation, created_by=user_3, created_by_id='3'),
            Comment(id=3, appreciation=appreciation, created_by=user_4, created_by_id='4'),
        ]

        comment = Comment(id=5, appreciation=appreciation, created_by=current_user)

        with patch('snowflake.services.notification.current_user', current_user):
            notify_comment(comment)

            assert mock_persist.call_count == 4

            notified_users = []
            for call in mock_persist.call_args_list:
                notification = call[0][0]
                assert notification.object_id == '5'
                notified_users.append((notification.user_id, notification.type))

            assert notified_users == [
                ('1', TYPE_COMMENT_ON_APPRECIATION_RECEIVED),
                ('2', TYPE_COMMENT_ON_APPRECIATION_RECEIVED),
                ('3', TYPE_COMMENT_ON_APPRECIATION_COMMENTED),
                ('4', TYPE_COMMENT_ON_APPRECIATION_COMMENTED),
            ]


@patch('snowflake.services.notification.db.persist')
def test_notify_one_on_one_setup(mock_persist: Mock, app):
    with app.app_context():
        one_on_one = OneOnOne(id=1, created_by_id='100', user_id='1')

        notify_one_on_one_setup(one_on_one)

        assert mock_persist.called

        notification = mock_persist.call_args[0][0]

        assert notification.type == TYPE_ONE_ON_ONE_SETUP
        assert notification.user_id == '1'
        assert notification.object_id == '1'


@patch('snowflake.services.notification.db.persist')
def test_notify_one_on_one_action_item_added_notifies_other_party(mock_persist: Mock, app):
    with app.app_context():
        one_on_one = OneOnOne(id=1, created_by_id='100', user_id='1')
        action_item_1 = OneOnOneActionItem(id=1, one_on_one=one_on_one, created_by_id='100')

        with patch('snowflake.services.notification.current_user', User(id='100')):
            notify_one_on_one_action_item_added(action_item_1)

        assert mock_persist.called

        notification = mock_persist.call_args[0][0]

        assert notification.type == TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED
        assert notification.user_id == '1'
        assert notification.object_id == '1'

        action_item_2 = OneOnOneActionItem(id=2, one_on_one=one_on_one, created_by_id='1')

        with patch('snowflake.services.notification.current_user', User(id='1')):
            notify_one_on_one_action_item_added(action_item_2)

        assert mock_persist.called

        notification = mock_persist.call_args[0][0]

        assert notification.type == TYPE_ONE_ON_ONE_ACTION_ITEM_ADDED
        assert notification.user_id == '100'
        assert notification.object_id == '1'
