import re


def parse_hours(messages: str) -> int:
    """ Parse hours from /call message """
    matcher = re.match(r"/call[\s]*(\d+)", messages)
    if matcher is None:
        raise ValueError("Сообщение должно соответствовать шаблону /call hours")
    hours = int(matcher.group(1))
    if not 1 <= hours <= 24:
        raise ValueError("Количество часов должно быть от 1 до 24")
    
    return hours
