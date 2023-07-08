def block(string: str):
    return "```" + string + "```"


def quote(string: str):
    return ">>> " + string


def toURL(string1: str | list, string2: str | list):
    if isinstance(string1, list) and (len(string2) > 1 or isinstance(string2, list)):
        return ", ".join(["[%s](%s)" % (obj1, obj2) for obj1, obj2 in zip(string1, string2)])
    return "[%s](%s)" % (string1, string2)
