import socket as sk
from sys import stderr
from typing import Union
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from re import findall
from json import loads as js_loads
from json import dumps


class PrintingSocket(sk.socket):
    def recv_print(self) -> bytes:
        msg = self.recv()
        try:
            decoded = msg.decode()
            print(decoded)
        except UnicodeDecodeError:
            print("Not printable!")
        return msg
    
    def recv(self) -> bytes:
        return super().recv(4096)

    def send_print(self, data: bytes) -> int:
        try:
            msg = data.decode()
            print(msg)
        except UnicodeDecodeError:
            print("Not printable!")
        return self.send(data)

    def send_print_dict(self, data: dict) -> int:
        try:
            print(data)
        except UnicodeDecodeError:
            print("Not printable!")
        return self.send(dumps(data).encode())
    
    def send_dict(self, data: dict) -> int:
        return self.send(dumps(data).encode())


def get_blocks(ciphertext: str, size: int = 16) -> list:
    """_summary_
    Splits ciphertext into 16 byte blocks (alter with size)

    Args:
        ciphertext (str): from `get_ciphertext`

    Returns:
        list: list of ciphertext blocks, each of len 32 (16 bytes)
    """
    size *= 2
    return [ciphertext[i : i + size] for i in range(0, len(ciphertext), size)]


def ints_to_hex(int_list):
    ret = ""
    for n in int_list:
        ret += hex(n)[2:].zfill(2)
    return ret


def xor_strings(s1: str, s2: str) -> str:
    """_summary_
    XORs 2 hexadecimal strings

    Args:
        s1: str
        s2: str

    Returns:
        str: an hexadecimal string, result of both XORs
    """
    try:
        int(s1, 16)
    except ValueError:
        print(rf"ERROR: The first parameter is not an hexadecimal string", file=stderr)
        exit(1)

    try:
        int(s2, 16)
    except ValueError:
        print(rf"ERROR: The second parameter is not an hexadecimal string", file=stderr)
        exit(1)

    res_len = min(len(s1), len(s2)) - (min(len(s1), len(s2)) % 2)
    s1_hex_list = [s1[i : i + 2] for i in range(0, res_len, 2)]
    s2_hex_list = [s2[i : i + 2] for i in range(0, res_len, 2)]
    res_list = []

    for c1, c2 in zip(s1_hex_list, s2_hex_list):
        res_list.append(hex(int(c1, 16) ^ int(c2, 16))[2:].rjust(2, "0"))

    return "".join(res_list)


def hex_to_ascii(s: str) -> str:
    """_summary_
    Converts an hex string to an ASCII string

    Args:
        s (str): hex string

    Returns:
        str: ASCII string
    """
    return bytes.fromhex(s).decode()


def ascii_to_hex(s: str) -> str:
    """_summary_
    Converts an ASCII string to an hex string

    Args:
        s (str): ASCII string

    Returns:
        str: hex string
    """
    return s.encode().hex()

def hex_to_bin(h: str) -> bytes:
    """_summary_
    Converts hex to binary

    Args:
        h (str): Hexadecimal string

    Returns:
        bytes: hex bytes
    """
    return bytes.fromhex(h)


def get_flag_in_message(m: Union[bytes, str]) -> str:
    if type(m) == str:
        m = m.encode()

    s = m.index(b"crypto{")
    e = m.index(b"}")
    return m[s : e + 1].decode()


def get_n_e_from_rsa_pubkey(pubkey: str) -> tuple[int, int]:
    # Load the RSA public key from PEM format
    public_key = serialization.load_pem_public_key(pubkey, backend=default_backend())

    # Extract n and e parameters
    n = public_key.public_numbers().n
    e = public_key.public_numbers().e

    return n, e


def parse_dicts(string):
    # Regular expression to find dictionaries
    pattern = rb"\{[^{}]*\}"
    # Find all dictionaries in the string
    dicts = findall(pattern, string)
    parsed_dicts = []
    for d in dicts:
        # Parse each dictionary string into a Python dictionary
        parsed_dict = js_loads(d)
        parsed_dicts.append(parsed_dict)
    return parsed_dicts

# https://github.com/orisano/owiener/blob/master/owiener.py#L26
def isqrt(n: int) -> int:
    """
    ref: https://en.wikipedia.org/wiki/Integer_square_root
    
    >>> isqrt(289)
    17
    >>> isqrt(2)
    1
    >>> isqrt(1000000 ** 2)
    1000000
    """
    if n == 0:
        return 0

    # ref: https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Rough_estimation
    x = 2 ** ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


# https://github.com/orisano/owiener/blob/master/owiener.py#L49
def is_perfect_square(n: int) -> bool:
    """
    ref: https://hnw.hatenablog.com/entry/20140503

    >>> is_perfect_square(100)
    True
    
    >>> is_perfect_square(2000000000000000000000000000 ** 2)
    True

    >>> is_perfect_square(2000000000000000000000000000 ** 2 + 1)
    False
    """
    sq_mod256 = (1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
    if sq_mod256[n & 0xff] == 0:
        return False

    mt = (
        (9, (1,1,0,0,1,0,0,1,0)),
        (5, (1,1,0,0,1)),
        (7, (1,1,1,0,1,0,0)),
        (13, (1,1,0,1,1,0,0,0,0,1,1,0,1)),
        (17, (1,1,1,0,1,0,0,0,1,1,0,0,0,1,0,1,1))
    )
    a = n % (9 * 5 * 7 * 13 * 17)
    if any(t[a % m] == 0 for m, t in mt):
        return False

    return isqrt(n) ** 2 == n