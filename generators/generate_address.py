import random
from fakeData.municipalities import municipalities


def generate_address(self) -> str:
    street = random.choice(self.streets)
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
