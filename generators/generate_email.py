import random
from generators.generate_names import generate_name

def generate_email() -> str:
    name = generate_name()
    clean_name = ''.join(c for c in name if c.isalnum()).lower()
    domain = random.choice([
        "example.com", "test.com.br", "email.com",
        "gmail.com", "outlook.com", "yahoo.com", "hotmail.com"
    ])
    return f"{clean_name}@{domain}"
