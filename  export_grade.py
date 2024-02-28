from json import loads as json_loads
from os import system
from time import sleep

from sage.all import *

from utils.utils import PrintingSocket


def exploit(p, g, A, B) -> int:
    F = GF(p)
    g, A = F(g), F(A)
    a = discrete_log(A, g)
    return pow(B, int(a), p)


with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13379))
    s.recv_print()
    s.recv_print()
    s.send_print(b'{"supported": ["DH64"]}')
    s.recv_print()
    s.recv_print()
    s.send_print(b'{"chosen": "DH64"}')
    sleep(2)
    params = "".join(s.recv_print().decode().split("Alice: ")[1:])
    alice_params = json_loads(params.split("\n")[0])
    general_params = json_loads(params.split("\n")[2].split("from ")[1])
    B = int(json_loads(params.split("Bob: ")[1:][0].split("\n")[0])["B"], 16)
    p = int(alice_params["p"], 16)
    g = int(alice_params["g"], 16)
    A = int(alice_params["A"], 16)
    iv = general_params["iv"]
    flag = general_params["encrypted_flag"]
    print(f"p={p}, g={g}, A={A}")
    print(f"iv={iv}, flag={flag}")

    # 64 bit DH is not secure, the BSGS algorithm (Shanks' Algorithm)
    # Reduces the naive brute force approach to O(sqrt(n)) by using a hashmap
    # and representing the exponent a as im+j.
    # Hence the search will take approx 2**32 steps.
    s = exploit(p, g, A, B)

    system(f"python3 utils/decrypt.py {s} {iv} {flag}")
