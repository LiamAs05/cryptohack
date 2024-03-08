from utils.utils import PrintingSocket
from time import sleep
from json import loads, dumps
from copy import deepcopy
from os import system

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13373))
    s.recv_print()

    sleep(1.5)
    params, t = s.recv_print().split(b"Intercepted from Bob: ")

    alice_params = loads(params.decode())
    bob_params, t = t.split(b"Intercepted from Alice:")
    bob_params = loads(bob_params.decode())
    alice_flag, _ = t.split(b"Bob")
    alice_flag = loads(alice_flag.decode())

    to_send = deepcopy(alice_params)
    to_send["A"] = "0x1"

    s.send_print(dumps(to_send).encode())
    sleep(1)
    t = s.recv_print().split(b"Bob says to you: ")
    _, bob_params_2, bob_flag_2 = t
    bob_flag_2 = loads(bob_flag_2.decode())
    bob_params_2 = loads(bob_params_2.decode())

    print("Start of Exploitation".center(60, "-"))
    iv = bob_flag_2["iv"]
    flag = bob_flag_2["encrypted"]
    system(f"python3 utils/decrypt.py 1 {iv} {flag}")
