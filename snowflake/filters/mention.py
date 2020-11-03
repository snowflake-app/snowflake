import re

from markupsafe import Markup

from snowflake.models import User


def add_mentions(text: str):
    mentions = set(re.findall(r'@[a-zA-Z0-9._]+', text))

    replacement = {}
    for mention in mentions:
        username = mention[1:]
        user = User.get_by_username(username)
        if user is None:
            continue

        replacement[mention] = f'<a href="/profile/{username}">{mention}</a>'

    for k, v in replacement.items():
        text = text.replace(k, v)

    return Markup(text)
