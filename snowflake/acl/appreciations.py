from ..models import Appreciation


def can_view_appreciations():
    return True


def can_create_appreciations():
    return True


def can_view_appreciation(_: Appreciation):
    return True
