import requests
from utils import utils 
from datetime import timedelta, datetime

def get_cookie():
    return requests.get("https://aes.cryptohack.org/flipping_cookie/get_cookie/").json()["cookie"]


def main():
    cookie = utils.get_blocks(get_cookie())
    iv = cookie[0]
    cookie = ''.join(cookie[1:])
    expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    mal = utils.xor_strings(utils.ascii_to_hex(f"admin=True;;expiry={expires_at}"), utils.ascii_to_hex(f"admin=False;expiry={expires_at}"))
    malicious_iv = utils.xor_strings(iv, mal) 
    print(
        requests.get(
            rf"https://aes.cryptohack.org/flipping_cookie/check_admin/{cookie}/{malicious_iv}"
        ).json()["flag"]
    )


if __name__ == "__main__":
    main()
