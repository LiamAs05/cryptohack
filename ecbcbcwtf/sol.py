from requests import get
from urllib.parse import urljoin

ENC_URL = r"https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/"
DEC_URL = r"https://aes.cryptohack.org/ecbcbcwtf/decrypt/"


def xor_strings(string1, string2):
    return hex(int(string1, 16) ^ int(string2, 16))


def get_blocks(ciphertext: str) -> list:
    """_summary_
    Splits ciphertext into 16 byte blocks

    Args:
        ciphertext (str): from `get_ciphertext`

    Returns:
        list: list of ciphertext blocks, each of len 32 (16 bytes)
    """
    return [ciphertext[i : i + 32] for i in range(0, len(ciphertext), 32)]


def get_flag_enc() -> str:
    """_summary_
    Given a payload, sends a GET request to /ecbcbcwtf/encrypt_flag/

    Args:
        payload (str): plaintext

    Returns:
        str: ciphertext
    """
    return get(ENC_URL).json()["ciphertext"]


def decrypt(payload: str) -> str:
    """_summary_
    Given a payload, sends a GET request to /ecbcbcwtf/decrypt/<payload>

    Args:
        payload (str): plaintext

    Returns:
        str: ciphertext
    """
    return get(urljoin(DEC_URL, payload)).json()["plaintext"]


def main():
    flag = get_flag_enc()
    blocks = get_blocks(flag)
    iv = blocks[0]
    first_part = xor_strings(decrypt(blocks[1]), iv)[2:]
    second_part = xor_strings(decrypt(blocks[2]), blocks[1])[2:]
    print(first_part, second_part)


if __name__ == "__main__":
    main()
