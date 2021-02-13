from datetime import datetime

_MINUTE = 60
_HOUR = _MINUTE * 60
_DAY = _HOUR * 24
_MONTH = 30 * _DAY


def humanize_time(date: datetime):
    now = datetime.now()

    if now.year != date.year:
        return date.strftime("%-m %b, %y")

    interval = (now - date).total_seconds()

    suffix = 'ago' if interval > 0 else 'later'

    interval = abs(interval)

    if interval < _MINUTE:
        return "Just now"

    if interval < _HOUR:
        return f'{int(interval / _MINUTE)}m {suffix}'

    if interval < _DAY:
        return f'{int(interval / _HOUR)}h {suffix}'

    if interval < _MONTH:
        return f'{int(interval / _DAY)}d {suffix}'

    return f'{date.strftime("%-m %b")} {suffix}'
