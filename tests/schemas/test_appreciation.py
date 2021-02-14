from datetime import datetime
from unittest.mock import patch

from snowflake.models import User, Like, Appreciation, Comment, Mention
from snowflake.schemas.appreciation import LikeSchema, AppreciationSchema

time = datetime.now()

user = User(id='12345', name='Hello', designation='Developer',
            team_name='Engineering', username='hello',
            email='hello@example.com',
            created_at=time,
            profile_pic='https://example.com/picture.jpg')

appreciation = Appreciation(
    id=1,
    content='Hello World',
    created_at=time,
    created_by=user,
)

appreciation.likes = [
    Like(id=1, created_by=user, appreciation=appreciation, created_at=time),
    Like(id=2, created_by=user, appreciation=appreciation, created_at=time)
]
appreciation.comments = [
    Comment(id=1, content='Hello World', created_by=user, appreciation=appreciation)]
appreciation.mentions = [Mention(id=1, appreciation=appreciation, user=user)]


def test_like_schema():
    schema = LikeSchema()

    like = Like(
        id=1,
        created_by=user,
        created_at=time,
        appreciation=appreciation
    )

    expected = {
        'createdBy': {
            'createdAt': time.isoformat(),
            'designation': 'Developer',
            'email': 'hello@example.com',
            'name': 'Hello',
            'profilePic': 'https://example.com/picture.jpg',
            'teamName': 'Engineering',
            'username': 'hello'},
        'id': 1
    }

    assert schema.dump(like) == expected


def test_appreciation_schema(app):
    with app.app_context():
        with patch('snowflake.models.like.Like.query') as like_query, \
                patch('snowflake.models.comment.Comment.query') as comment_query:
            like_query.filter_by(appreciation=appreciation).count.return_value = 2
            comment_query.filter_by(appreciation=appreciation).count.return_value = 1

            schema = AppreciationSchema()

            expected = {
                'commentCount': 1,
                'content': 'Hello World',
                'createdAt': time.isoformat(),
                'createdBy': {
                    'createdAt': time.isoformat(),
                    'designation': 'Developer',
                    'email': 'hello@example.com',
                    'name': 'Hello',
                    'profilePic': 'https://example.com/picture.jpg',
                    'teamName': 'Engineering',
                    'username': 'hello'},
                'id': 1,
                'likeCount': 2,
                'mentions': [
                    {
                        'user': {
                            'createdAt': time.isoformat(),
                            'designation': 'Developer',
                            'email': 'hello@example.com',
                            'name': 'Hello',
                            'profilePic': 'https://example.com/picture.jpg',
                            'teamName': 'Engineering',
                            'username': 'hello'
                        }
                    }
                ]
            }

            assert schema.dump(appreciation) == expected
