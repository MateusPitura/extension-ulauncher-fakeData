import random
from src.utils.generate_random_number import generate_random_number
from src.fakeData.valid_ddd import valid_ddd


def generate_home_phone():
    ddd = str(random.choice(valid_ddd))

    first_digit = random.choice(["2", "3", "4", "5"])
    number = first_digit + generate_random_number(7)

    return f"({ddd}) {number[:4]}-{number[4:]}"
