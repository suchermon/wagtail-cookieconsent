import re


def underscore_string(value):
    if not isinstance(value, str) or value == '':
        raise ValueError

    return re.sub('\W+', ' ', value.lower()).strip().replace(' ', '_')
