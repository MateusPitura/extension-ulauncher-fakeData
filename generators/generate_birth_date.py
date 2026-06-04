import random
import datetime


def generate_birth_date(start="1950-01-01", end="2010-12-31") -> str:
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    birth_date = start_date + datetime.timedelta(days=random_days)
    return birth_date.strftime("%d/%m/%Y")
