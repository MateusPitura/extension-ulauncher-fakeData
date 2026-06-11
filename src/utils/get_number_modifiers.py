import re

def parse_number(text):
    min_value = None
    max_value = None
    digit_count = None

    if not text.lower().startswith("number "):
        return min_value, max_value, digit_count

    parts = text.split()[1:]

    if len(parts) == 1 and parts[0].isdigit():
        digit_count = int(parts[0])
        return min_value, max_value, digit_count

    for part in parts:
        match = re.fullmatch(r"([<>])(\d+)", part)
        if not match:
            raise ValueError("Invalid format")

        op, value = match.groups()
        value = int(value)

        if op == ">":
            min_value = value
        else:
            max_value = value

    return min_value, max_value, digit_count