import json
import requests
import re

cards = []

for _ in range(10):
    response = requests.post(
        "https://www.4devs.com.br/ferramentas_online.php",
        data={
            "acao": "gerar_cc",
            "pontuacao": "S",
            "bandeira": "master",
        },
        timeout=10
    )
    response.raise_for_status()

    card = {
        "Number": re.search(r'id="cartao_numero".*?>(.*?)<', response.text, re.S).group(1).strip(),
        "Expiration Date": re.search(r'id="data_validade".*?>(.*?)<', response.text, re.S).group(1).strip(),
        "CVV": re.search(r'id="codigo_seguranca".*?>(.*?)<', response.text, re.S).group(1).strip(),
    }

    cards.append(card)

print(json.dumps(cards, ensure_ascii=False, indent=4))
