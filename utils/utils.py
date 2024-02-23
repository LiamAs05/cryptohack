from sys import stderr


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
    return bytearray.fromhex(s).decode()
