from src.utils.generate_random_number import generate_random_number


def generate_postal_code(with_dash=True) -> str:
    postal = generate_random_number(8)
    if with_dash:
        return f"{postal[:5]}-{postal[5:]}"
    return postal
