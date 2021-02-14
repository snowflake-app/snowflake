from datetime import datetime

from snowflake import db
from snowflake.models import User


def test_autocomplete_should_return_matching_users(client, app):
    created_at = datetime.now()

    with app.app_context():
        with db.transaction():
            User.query.delete()
            db.persist(User(
                id='1',
                name="John Doe",
                designation='Developer',
                team_name='Engineering',
                email='john.doe@example.com',
                profile_pic='https://example.com/avatars/1.jpg',
                username='john.doe',
                created_at=created_at))

            db.persist(User(
                id='2',
                name="John Adams",
                designation='Developer',
                team_name='Engineering',
                email='john.adams@example.com',
                profile_pic='https://example.com/avatars/1.jpg',
                username='john.adams',
                created_at=created_at))

            db.persist(User(
                id='3',
                name="Not John",
                designation='Developer',
                team_name='Engineering',
                email='not.john@example.com',
                profile_pic='https://example.com/avatars/1.jpg',
                username='john.not.john',
                created_at=created_at))

            db.persist(User(
                id='4',
                name="Johnathan Lion",
                designation='Developer',
                team_name='Engineering',
                email='johnathan@example.com',
                profile_pic='https://example.com/avatars/1.jpg',
                username='lion.johnathan',
                created_at=created_at))

            db.persist(User(
                id='5',
                name="Tom Riddle",
                designation='Dark Lord',
                team_name='Engineering',
                email='voldemort@example.com',
                profile_pic='https://example.com/avatars/1.jpg',
                username='voldemort',
                created_at=created_at))

    response = client.get('/api/users/_autocomplete?q=john')

    assert response.status_code == 200
    assert response.json == [
        {
            'createdAt': created_at.isoformat(),
            'designation': 'Developer',
            'email': 'john.doe@example.com',
            'name': 'John Doe',
            'profilePic': 'https://example.com/avatars/1.jpg',
            'teamName': 'Engineering',
            'username': 'john.doe'},
        {
            'createdAt': created_at.isoformat(),
            'designation': 'Developer',
            'email': 'john.adams@example.com',
            'name': 'John Adams',
            'profilePic': 'https://example.com/avatars/1.jpg',
            'teamName': 'Engineering',
            'username': 'john.adams'},
        {
            'createdAt': created_at.isoformat(),
            'designation': 'Developer',
            'email': 'not.john@example.com',
            'name': 'Not John',
            'profilePic': 'https://example.com/avatars/1.jpg',
            'teamName': 'Engineering',
            'username': 'john.not.john'},
        {
            'createdAt': created_at.isoformat(),
            'designation': 'Developer',
            'email': 'johnathan@example.com',
            'name': 'Johnathan Lion',
            'profilePic': 'https://example.com/avatars/1.jpg',
            'teamName': 'Engineering',
            'username': 'lion.johnathan'
        }
    ]


def test_autocomplete_should_return_400_if_q_is_not_given(client):
    response = client.get('/api/users/_autocomplete')

    assert response.status_code == 400
    assert response.json == {
        'message': "missing search term 'q'"
    }
