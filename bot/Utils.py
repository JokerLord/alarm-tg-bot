import re


def parse_call_hours(message: str) -> int:
    """Parse hours from /call message"""
    matcher = re.match(r"/call[\s]*(\d+)", message)
    if matcher is None:
        raise ValueError("Сообщение должно соответствовать шаблону /call hours")
    hours = int(matcher.group(1))
    if not hours > 0:
        raise ValueError("Количество часов должно быть больше 0")

    return hours
