import random
from src.generators.generate_random_number import generate_random_number
from src.fakeData.valid_ddd import valid_ddd


def generate_mobile_phone():
    ddd = str(random.choice(valid_ddd))

    number = "9" + generate_random_number(digit_count=8)

    return f"({ddd}) {number[:5]}-{number[5:]}"
