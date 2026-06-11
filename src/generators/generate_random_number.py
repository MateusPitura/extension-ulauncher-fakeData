import random
import string


def generate_random_number(min_value=None, max_value=None, digit_count=None):
    if digit_count is not None:
        if digit_count < 1:
            raise ValueError("digit_count must be greater than 0")

        return ''.join(random.choice(string.digits) for _ in range(digit_count))

    if min_value is None:
        min_value = 0

    if max_value is None:
        max_value = 999999999

    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")

    return random.randint(min_value, max_value)
