from datetime import datetime, timedelta
from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad, unpad


def get_blocks(ciphertext: str) -> list:
    """_summary_
    Splits ciphertext into 16 byte blocks

    Args:
        ciphertext (str): from `get_ciphertext`

    Returns:
        list: list of ciphertext blocks, each of len 32 (16 bytes)
    """
    return [ciphertext[i : i + 32] for i in range(0, len(ciphertext), 32)]


def main():
    KEY = os.urandom(16)
    # expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    # mock_cookie = f"admin=False;expiry={expires_at}".encode()
    # cookie_with_iv = "cd636213f6f4b38e900b5a332bccf396fdc4994cca567159590e7ac3a1c80991ea3e185905d9f9d7d86709556b8054f1"
    # iv, b1, b2 = get_blocks(cookie_with_iv)
    # admin_equals = (b1[:12], iv)

    # print("IV:", iv)
    # print("b1:", b1, "p1:", mock_cookie[:16])
    # print("b2:", b2, "p1:", mock_cookie[16:32])

    expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    cookie = f"admin=False;expiry={expires_at}".encode()

    iv = b'\x00'*16
    padded = pad(cookie, 16)
    print(padded)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    ciphertext = iv.hex() + encrypted.hex()

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    unpadded = unpad(decrypted, 16)
    print({"cookie": ciphertext})
    print(unpadded)


if __name__ == "__main__":
    main()
