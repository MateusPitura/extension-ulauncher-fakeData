import random
from utils.generate_random_number import generate_random_number


def generate_phone(with_ddd=True) -> str:
    ddd = generate_random_number(2) if with_ddd else ""
    if random.choice([True, False]):
        number = "9" + generate_random_number(8)
    else:
        number = generate_random_number(8)
    if ddd:
        if len(number) == 9:
            return f"({ddd}) {number[:5]}-{number[5:]}"
        return f"({ddd}) {number[:4]}-{number[4:]}"
    return number
