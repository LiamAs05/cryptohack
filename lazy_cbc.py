from utils.utils import get_blocks, xor_strings, hex_to_ascii
from requests import get


def main():
    URL = r"https://aes.cryptohack.org/lazy_cbc/"
    res = get(URL + "receive/" + "00" * 16 * 2).json()["error"]
    d_c, p = get_blocks(res[len("Invalid plaintext: ") :])
    key = xor_strings(d_c, p)
    flag = get(URL + rf"get_flag/{key}").json()["plaintext"]

    print(hex_to_ascii(flag))


if __name__ == "__main__":
    main()
