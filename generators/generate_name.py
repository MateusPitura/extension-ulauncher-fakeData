import random

def generate_name(self) -> str:
    first = random.choice(self.first_names)
    last = random.choice(self.last_names)
    return f"{first} {last}"
