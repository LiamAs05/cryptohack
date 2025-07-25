from os import system
from time import sleep
from utils.utils import PrintingSocket, parse_dicts

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13380))
    sleep(1)
    alice_params, bob_params, flag_params = parse_dicts(s.recv_print())
    A = int(alice_params["A"], 16)
    B = int(bob_params["B"], 16)
    g = int(alice_params["g"], 16)
    p = int(alice_params["p"], 16)
    C = pow(g, p - 2, p)
    flag = flag_params["encrypted"]
    iv = flag_params["iv"]
    ss = (A * B * C) % p  # By Fermat's little theorem, g**p = g mod p
    # We also know that DH in additive groups calculates A=g*a instead of g**a
    # So we have g*a and g*b, we can compute A*B=(g*a)(g*b)=a*b*g**2
    # The Shared Secret is a*b*g, and using Fermat's little theorom we can obtain it
    # A*B*C=(g*a)(g*b)(g*p-2)=a*b*g**(2+p-2)=a*b*g**p = a*b*g = Shared Secret

system(f"python3 utils/decrypt.py {ss} {iv} {flag}")
