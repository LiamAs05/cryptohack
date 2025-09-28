import random
import re
import string

from Cryptodome.Util.number import isPrime

from utils.utils import PrintingSocket


def has_numbers(s):
    return any(char.isdigit() for char in s)


def has_lower(s):
    return any(char.isupper() for char in s)


def has_upper(s):
    return any(char.islower() for char in s)


def main():
    prod = 1
    s = 0
    letters = ""

    while (
        not isPrime(prod)
        or not isPrime(s)
        or not has_numbers(letters)
        or not has_lower(letters)
        or not has_upper(letters)
    ):
        prod *= ord(choice := random.choice(string.ascii_letters + string.digits))
        prod %= 2**64
        letters += choice
        s += ord(choice)
        s %= 2**64
        if len(letters) > 20:
            letters = "AA"
            prod = 65 * 65
            s = 65 + 65

    with PrintingSocket() as s:
        s.connect(("socket.cryptohack.org", 13400))
        s.recv_print()
        s.send_dict({"password": letters})
        s.recv_print()


if __name__ == "__main__":
    main()
