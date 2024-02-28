from json import loads
from math import ceil, sqrt
from os import system
from time import sleep

from utils.utils import PrintingSocket


# https://en.wikipedia.org/wiki/Baby-step_giant-step
def baby_step_giant_step(p, g, A) -> int:
    d = {}
    m = ceil(sqrt(p - 1))
    for j in range(m):
        d[pow(g, j, p)] = j
    print("Finished baby-step")

    c = pow(g, m * (p - 2), p)
    for i in range(m):
        temp = (A * pow(c, i, p)) % p
        if t := d.get(temp, None):
            return i * m + t
        temp = temp * c % p
    print("Finished Giant Step")


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
    alice_params = loads(params.split("\n")[0])
    general_params = loads(params.split("\n")[2].split("from ")[1])

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
    print(s := baby_step_giant_step(p, g, A))
    system(f"python3 utils/decrypt.py {s} {iv} {flag}")
