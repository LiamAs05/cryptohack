from copy import deepcopy
from os import system
from time import sleep

from Crypto.Util import number

from utils.utils import PrintingSocket, parse_dicts


def get_hint(s, alice_params):
    my_params = deepcopy(alice_params)
    my_params["g"] = "0x2"
    my_params["A"] = "0x4"

    s.send_print_dict(my_params)
    sleep(1)
    sec_bob_params, sec_flag_params = parse_dicts(s.recv_print())

    p = int(my_params["p"], 16)
    B = int(sec_bob_params["B"], 16)
    ss = pow(B, 2, p)

    iv = sec_flag_params["iv"]
    flag = sec_flag_params["encrypted"]

    system(f"python3 utils/decrypt.py {ss} {iv} {flag}")


def main():
    with PrintingSocket() as s:
        s.connect(("socket.cryptohack.org", 13378))
        sleep(1)
        alice_params, bob_params, flag_params = parse_dicts(s.recv_print())
        get_hint(s, alice_params)


if __name__ == "__main__":
    main()
