import os


def block(string: str):
    return "```" + string + "```"


def quote(string: str):
    return ">>> " + string


def toURL(string1: str | list, string2: str | list):
    if isinstance(string1, list) and (len(string2) > 1 or isinstance(string2, list)):
        return ", ".join(["[%s](%s)" % (obj1, obj2) for obj1, obj2 in zip(string1, string2)])
    return "[%s](%s)" % (string1, string2)



def sequence(material_path:str, target_directory:str):
    count = sum([1 for path in os.listdir(target_directory) if path == material_path])
    name, ext = os.path.splitext(material_path)

    return "%s-%s%s" % (name, count, ext) if count == 0 else material_path

