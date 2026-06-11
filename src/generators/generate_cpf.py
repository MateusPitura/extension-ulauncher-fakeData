from src.generators.generate_random_number import generate_random_number
from src.utils.calculate_digit import calculate_digit


def generate_cpf(formatted=True) -> str:
    nine_digits = generate_random_number(digit_count=9)
    first_weights = list(range(10, 1, -1))
    first_digit = calculate_digit(nine_digits, first_weights)
    second_weights = list(range(11, 1, -1))
    second_digit = calculate_digit(nine_digits + first_digit, second_weights)
    cpf = nine_digits + first_digit + second_digit
    if formatted:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf
