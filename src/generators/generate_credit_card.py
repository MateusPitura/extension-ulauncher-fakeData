import random
from src.fakeData.credit_card import credit_card


def generate_credit_card(formatted=True, date_format="dd/mm/yyyy"):
    credit_card_aux = random.choice(credit_card).copy()

    if not formatted:
        credit_card_aux["Number"] = credit_card_aux["Number"].replace(" ", "")

    if date_format == "YYYY-MM-DD":
        credit_card_aux["Expiration Date"] = credit_card_aux["Expiration Date"].strftime(
            "%Y-%m-%d"
        )

    full_credit_card = credit_card_aux

    credit_card_string = f"{full_credit_card['Number']}, {full_credit_card['Expiration Date']}, {full_credit_card['CVV']}"

    return (credit_card_string, full_credit_card)
