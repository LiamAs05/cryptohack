from requests import get

# Everything is in the writeup


def main():
    cookie = "2483c5de09129100db629163c54729a5951485f993a7a42fc548cac569f52ad8"
    malicious_iv = "edd2553317f66948738e1dc3970a1075"
    print(
        get(
            rf"https://aes.cryptohack.org/flipping_cookie/check_admin/{cookie}/{malicious_iv}"
        ).json()["flag"]
    )


if __name__ == "__main__":
    main()
