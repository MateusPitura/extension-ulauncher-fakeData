import random
import string


def generate_random_number(count):
    return ''.join(random.choice(string.digits) for _ in range(count))
