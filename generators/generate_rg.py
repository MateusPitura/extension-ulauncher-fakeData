from src.utils.generate_random_number import generate_random_number

def generate_rg(formatted=False) -> str:
    rg = generate_random_number(9)
    if formatted:
        return f"{rg[:2]}.{rg[2:5]}.{rg[5:8]}-{rg[8]}"
    return rg
