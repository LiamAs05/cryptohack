from binascii import hexlify
from string import ascii_lowercase, digits, punctuation
from urllib.parse import urljoin

from requests import get

from utils.utils import get_blocks

URL = r"https://aes.cryptohack.org/ecb_oracle/encrypt/"
ALLOWED_CHARACTERS = ascii_lowercase + punctuation + digits


def get_ciphertext(payload: str) -> str:
    """_summary_
    Given a payload, sends a GET request to /ecb_oracle/encrypt/<payload>

    Args:
        payload (str): plaintext

    Returns:
        str: ciphertext
    """
    return get(urljoin(URL, payload)).json()["ciphertext"]


def find_flag_len() -> int:
    """_summary_
    Gets the len of the flag.

    Returns:
        int: flag len
    """
    byte_num = 1
    payload = "00"
    data = get_ciphertext(payload * byte_num)
    data_len = len(data)

    while len(data) == data_len:
        data_len = len(data)
        byte_num += 1
        data = get_ciphertext(payload * byte_num)

    byte_num -= 1  # last increment increased the number of blocks, so we decrement

    return data_len // 2 - byte_num


def encrypt_plaintext_with_nulls(plaintext: str) -> str:
    """_summary_
    Given a plaintext, creates and returns a payload containing:
    0000...plaintext
    where plaintext is hexlified

    Args:
        plaintext (str)

    Returns:
        str: payload to encrypt
    """
    hex_plaintext = hexlify(
        plaintext.encode()
    ).decode()  # convert payload to a hex string
    payload = "00" * (32 - len(plaintext)) + hex_plaintext
    return payload


def leak_chars_from_flag(n: int):
    """_summary_
    Creates a payload to leak n first chars of flag

    Args:
        n (int): no. of chars

    Returns:
        str: payload to encrypt
    """
    return "00" * (32 - n)


def exploit(flag_len: int):
    """_summary_
    Using the functions defined above, finds the flag

    Args:
        flag_len (int): length of the flag

    Returns:
        str: flag in plaintext
    """
    plaintext = ""

    for i in range(1, flag_len):
        leak = get_blocks(get_ciphertext(leak_chars_from_flag(i)))
        for j in ALLOWED_CHARACTERS:
            cipher = get_blocks(
                get_ciphertext(encrypt_plaintext_with_nulls(plaintext[-16:] + j))
            )

            if leak[1] == cipher[1]:
                plaintext += j
                break
        print(plaintext)
    return plaintext


def main():
    flag_len = find_flag_len()
    print(exploit(flag_len))


if __name__ == "__main__":
    main()
