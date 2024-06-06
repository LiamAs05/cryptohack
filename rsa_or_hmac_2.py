from base64 import b64decode

import jwt
from Crypto.Util.number import bytes_to_long
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from requests import get


def main():
    url = r"https://web.cryptohack.org/rsa-or-hmac-2/create_session/"
    e = 0x10001  # Generated by openssl rsa -RSAPublicKey_out
    N = 2**2048 + 1
    h1, d1, s1 = get(url + r"0").json()["session"].split(".")
    tok1_no_sig = h1 + "." + d1

    sig1 = bytes_to_long(b64decode(s1))  # sig1 = (tok1_no_sig)**d % n

    hash1 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hash1.update(tok1_no_sig.encode())  # Assuming the JWT token is in string format
    hash1 = bytes_to_long(hash1.finalize())

    # public_key = rsa.RSAPublicNumbers(e, N)

    # pem = public_key.public_key().public_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PublicFormat.SubjectPublicKeyInfo,
    # )
    # c = jwt.encode({"username": "0", "admin": True}, pem.decode(), algorithm="HS256")
    # print(c)


if __name__ == "__main__":  #
    main()
