import requests
import json
from src.utils.generate_random_number import generate_random_number

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

FIELDS_TO_KEEP = [
    "cep",
    "logradouro",
    "complemento",
    "bairro",
    "localidade",
    "uf",
    "estado",
    "regiao",
    "ibge",
    "ddd",
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

    address = {field: data.get(field, "") for field in FIELDS_TO_KEEP}

    # Add custom field
    address["numero"] = generate_random_number(4)

    addresses.append(address)

print(json.dumps(addresses, ensure_ascii=False, indent=4))