def str_to_int(string):
    return int("".join(filter(str.isdigit, [s for s in string])))
