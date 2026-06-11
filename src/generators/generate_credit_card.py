import random
from src.fakeData.credit_card import credit_card


def generate_credit_card():
    full_credit_card = random.choice(credit_card)

    credit_card_string = f"{full_credit_card['number']}, {full_credit_card['expiration_date']}, {full_credit_card['cvv']}"

    return (credit_card_string, full_credit_card)
