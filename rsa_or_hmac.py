from jwt import encode as jwtencode
from utils.utils import get_flag_in_message
from requests import get

pubkey = get("https://web.cryptohack.org/rsa-or-hmac/get_pubkey/").json()["pubkey"]
c = jwtencode({"username": "master", "admin": True}, pubkey, algorithm="HS256")
print(get_flag_in_message(get(rf"https://web.cryptohack.org/rsa-or-hmac/authorise/{c}").text))

# You're going to have to patch PyJWT to make this work
# For me it was v2.3.0, had to comment out lines 187-193 in algorithms.py
# Without it, an error will be raised and the new token won't be generated
# Which mitigates this vulnerability
