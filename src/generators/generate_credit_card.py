import random
from src.fakeData.credit_card import credit_card


def generate_credit_card():
    full_credit_card = random.choice(credit_card)

    credit_card_string = f"{full_credit_card['Number']}, {full_credit_card['Expiration Date']}, {full_credit_card['CVV']}"

    return (credit_card_string, full_credit_card)
