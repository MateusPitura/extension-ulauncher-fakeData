import random
import datetime

YEARS_20 = 20 * 365
YEARS_5 = 5 * 365


def generate_date(
    only_past=False,
    only_future=False,
    date_format="dd/mm/yyyy"
) -> str:
    if only_past and only_future:
        raise ValueError("only_past and only_future cannot both be True")

    today = datetime.date.today()

    if only_past:
        start_date = today - datetime.timedelta(days=YEARS_20)
        end_date = today
    elif only_future:
        start_date = today
        end_date = today + datetime.timedelta(days=YEARS_5)
    else:
        start_date = today - datetime.timedelta(days=YEARS_20)
        end_date = today + datetime.timedelta(days=YEARS_5)

    delta = (end_date - start_date).days
    random_days = random.randint(0, delta)

    random_date = start_date + datetime.timedelta(days=random_days)

    if date_format == "dd/MM/yyyy":
        return random_date.strftime("%d/%m/%Y")

    if date_format == "YYYY-MM-DD":
        return random_date.strftime("%Y-%m-%d")

    raise ValueError("Unsupported format")
