import random
import string

def generate_password(length=10, use_upper=True, use_digits=True, use_symbols=True):
    chars = list(string.ascii_lowercase)
    if use_upper:
        chars += list(string.ascii_uppercase)
    if use_digits:
        chars += list(string.digits)
    if use_symbols:
        chars += list("!@#$%^&*()-_=+[]{}")

    return "".join(random.choice(chars) for _ in range(length))
