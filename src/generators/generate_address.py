import random
from src.fakeData.address import address


def generate_address(formatted=True):
    address_aux = random.choice(address)

    if not formatted:
        address_aux['CEP'] = address_aux['CEP'].replace('-', '')

    full_address = address_aux

    address_string = f"{full_address['Street']}, {full_address['Number']} - {full_address['Neighborhood']}, {full_address['City']} - {full_address['UF']}, {full_address['CEP']}"

    return (address_string, full_address)
