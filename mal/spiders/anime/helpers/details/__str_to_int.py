def str_to_int(string: str) -> int:
    return int("".join(filter(str.isdigit, [s for s in string])))
