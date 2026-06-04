from utils.calculate_digit import calculate_digit
from utils.generate_random_number import generate_random_number


def generate_cnpj(formatted=True) -> str:
    root = generate_random_number(8)
    suffix = "0001"
    numbers = root + suffix
    first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    first_digit = calculate_digit(numbers, first_weights)
    second_weights = [6] + first_weights
    second_digit = calculate_digit(numbers + first_digit, second_weights)
    cnpj = numbers + first_digit + second_digit
    if formatted:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj
