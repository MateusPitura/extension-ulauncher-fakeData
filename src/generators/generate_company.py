import random
from src.fakeData.companies import companies


def generate_company():
    return random.choice(companies)
