from urllib.parse import urljoin

from requests import get

from utils.utils import get_blocks, hex_to_ascii, xor_strings

ENC_URL = r"https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/"
DEC_URL = r"https://aes.cryptohack.org/ecbcbcwtf/decrypt/"


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
    first_part = xor_strings(decrypt(blocks[1]), iv)
    second_part = xor_strings(decrypt(blocks[2]), blocks[1])
    res = first_part + second_part
    print(hex_to_ascii(res))


if __name__ == "__main__":
    main()
