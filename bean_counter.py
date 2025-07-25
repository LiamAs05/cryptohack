from requests import get

from utils.utils import hex_to_bin, xor_strings


def exploit(ciphertext: str):
    # First 16 bytes of a PNG file
    plaintext_start = r"89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52".replace(
        " ", ""
    )
    iv = xor_strings(plaintext_start, ciphertext)  # P XOR C = e(IV)
    ciphertext_blocks = [ciphertext[i : i + 32] for i in range(0, len(ciphertext), 32)]

    f = open("bean_flag.png", "wb")
    for block in ciphertext_blocks:
        dec = xor_strings(block, iv)  # C XOR e(IV) = P
        f.write(hex_to_bin(dec))

    f.close()


def get_ciphertext():
    return get("https://aes.cryptohack.org/bean_counter/encrypt").json()["encrypted"]


def main():
    c = get_ciphertext()
    exploit(c)
    print("Flag written to ./bean_flag.png")


if __name__ == "__main__":
    main()
