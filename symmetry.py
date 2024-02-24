from string import ascii_lowercase, digits, punctuation

from requests import get

from utils.utils import ascii_to_hex


def exploit(iv: str, ciphertext: str):
    curr_flag = r"crypto{"
    while "}" not in curr_flag:
        for i in digits + ascii_lowercase + punctuation:
            x = enc(ascii_to_hex(y := curr_flag + i), iv)
            if ciphertext.startswith(x):
                curr_flag = y
                print(curr_flag)
                break


def enc(p: str, iv: str):
    """_summary_
    Encryption

    Args:
        p (str): plaintext
        iv (str): IV

    Returns:
        str: ciphertext
    """
    ENC_URL = rf"https://aes.cryptohack.org/symmetry/encrypt/{p}/{iv}"
    return get(ENC_URL).json()["ciphertext"]


def main():
    URL = r"https://aes.cryptohack.org/symmetry/encrypt_flag/"
    c = get(URL).json()["ciphertext"]
    iv = c[:32]
    c = c[32:]
    exploit(iv, c)


if __name__ == "__main__":
    main()
