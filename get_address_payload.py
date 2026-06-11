import requests
import json
from src.generators.generate_random_number import generate_random_number

CEPS = [
    "01311-000",
    "22041-001",
    "30130-110",
    "80420-090",
    "90010-150",
    "88015-400",
    "50030-230",
    "60125-120",
    "74015-070",
]

addresses = []

for cep in CEPS:
    response = requests.get(
        f"https://viacep.com.br/ws/{cep}/json/",
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    if data.get("erro"):
        print(f"CEP not found: {cep}")
        continue

    address = {
        "CEP": data.get("cep", ""),
        "Street": data.get("logradouro", ""),
        "Number": generate_random_number(digit_count=4),
        "Complement": data.get("complemento", ""),
        "Neighborhood": data.get("bairro", ""),
        "City": data.get("localidade", ""),
        "UF": data.get("uf", ""),
        "State": data.get("estado", ""),
        "Region": data.get("regiao", ""),
        "IBGE Code": data.get("ibge", ""),
        "DDD": data.get("ddd", ""),
    }

    addresses.append(address)

print(json.dumps(addresses, ensure_ascii=False, indent=4))