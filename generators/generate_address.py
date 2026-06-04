import random
from fakeData.municipalities import municipalities
from fakeData.streets import streets


def generate_address():
    street = random.choice(streets)
    number = random.randint(1, 2000)
    complement = random.choice(
        [f"Apt {random.randint(1, 500)}", "", "House"])

    state = random.choice(list(municipalities.keys()))
    city = random.choice(municipalities[state])
    address = f"{street}, {number}"
    if complement:
        address += f", {complement}"
    address += f" - {city}/{state}"
    return address
