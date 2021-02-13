import re

from markupsafe import Markup

from snowflake.models import User


def add_mentions(text: str):
    mentions = set(re.findall(r'@[a-zA-Z0-9._]+', text))

    for mention in mentions:
        username = mention[1:]
        user = User.get_by_username(username)
        if user is None:
            continue

        text.replace(mention, f'<a href="/profile/{username}">{mention}</a>')

    return Markup(text)
