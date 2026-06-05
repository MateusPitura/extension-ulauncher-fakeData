import random
from src.fakeData.address import address


def generate_address():
    full_address = random.choice(address)

    address_string = f"{full_address['logradouro']}, {full_address['numero']} - {full_address['bairro']}, {full_address['localidade']} - {full_address['uf']}, {full_address['cep']}"

    return (address_string, full_address)
