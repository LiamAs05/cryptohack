from decimal import Decimal
from json import dumps
from math import gcd

from Crypto.Util.number import bytes_to_long


def main():
    url = r"https://web.cryptohack.org/rsa-or-hmac-2/"
    e = 2**16 + 1  # Assumption

    p1 = {"username": "1", "admin": False}
    p2 = {"username": "2", "admin": False}

    r1 = b"eyJ1c2VybmFtZSI6IjEiLCJhZG1pbiI6ZmFsc2V9"
    r2 = b"eyJ1c2VybmFtZSI6IjIiLCJhZG1pbiI6ZmFsc2V9"

    r1 = bytes_to_long(r1)
    r2 = bytes_to_long(r2)

    p1 = bytes_to_long(dumps(p1).encode())
    p2 = bytes_to_long(dumps(p2).encode())

    N = gcd(Decimal(p1**e - r1), Decimal(p2**e - r2))
    print(N)


if __name__ == "__main__":
    main()
