def calculate_digit(numbers, weights):
    total = sum(int(n) * p for n, p in zip(numbers, weights))
    remainder = total % 11
    return '0' if remainder < 2 else str(11 - remainder)
