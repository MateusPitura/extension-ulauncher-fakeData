import random
from src.fakeData.address import address


def generate_address():
    full_address = random.choice(address)

    address_string = f"{full_address['Rua']}, {full_address['Number']} - {full_address['Neighborhood']}, {full_address['City']} - {full_address['UF']}, {full_address['CEP']}"

    return (address_string, full_address)
