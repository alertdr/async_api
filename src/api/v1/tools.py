import re


def parse_brackets_params(param) -> dict:
    params = {}
    regex = r'(?P<op>.*)\[(?P<col>.*)\]'
    for key, value in dict(param).items():
        if m := re.search(regex, key):
            if m.group("op") in params:
                params[m.group("op")].update({m.group("col"): value})
            else:
                params.update({m.group("op"): {m.group("col"): value}})
        else:
            params.update({key: value})
    return params
