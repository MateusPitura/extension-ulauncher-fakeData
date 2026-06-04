import random
from fakeData.first_names import first_names
from fakeData.last_names import last_names


def generate_name():
    first = random.choice(first_names)
    last = random.choice(last_names)
    return f"{first} {last}"
