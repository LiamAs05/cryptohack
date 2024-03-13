from utils.utils import PrintingSocket
from time import sleep
from json import loads, dumps
from copy import deepcopy
from os import system


def part_one():
    with PrintingSocket() as s:
        s.connect(("socket.cryptohack.org", 13373))
        s.recv(4096)

        sleep(1.5)
        params, t = s.recv(4096).split(b"Intercepted from Bob: ")

        alice_params = loads(params.decode())
        bob_params, t = t.split(b"Intercepted from Alice:")
        bob_params = loads(bob_params.decode())
        alice_flag, _ = t.split(b"Bob")
        alice_flag = loads(alice_flag.decode())

        to_send = deepcopy(alice_params)
        to_send["A"] = "0x1"

        s.send(dumps(to_send).encode())
        sleep(1)
        t = s.recv(4096).split(b"Bob says to you: ")
        _, bob_params_2, bob_flag_2 = t
        bob_flag_2 = loads(bob_flag_2.decode())
        bob_params_2 = loads(bob_params_2.decode())

        iv = bob_flag_2["iv"]
        flag = bob_flag_2["encrypted"]
        system(f"python3 utils/decrypt.py 1 {iv} {flag}")


def part_two():
    with PrintingSocket() as s:
        s.connect(("socket.cryptohack.org", 13373))
        s.recv(4096)

        sleep(1.5)
        params, t = s.recv(4096).split(b"Intercepted from Bob: ")

        alice_params = loads(params.decode())
        bob_params, t = t.split(b"Intercepted from Alice:")
        bob_params = loads(bob_params.decode())
        alice_flag, _ = t.split(b"Bob")
        alice_flag = loads(alice_flag.decode())

        to_send = deepcopy(alice_params)
        to_send["g"] = to_send["A"]
        to_send["A"] = "0x0"
        s.send(dumps(to_send).encode())
        sleep(1)
        t = s.recv(4096).split(b"Bob says to you: ")
        _, bob_params_2, bob_flag_2 = t
        bob_flag_2 = loads(bob_flag_2.decode())
        bob_params_2 = loads(bob_params_2.decode())

        ss = int(bob_params_2["B"], 16)
        iv = alice_flag["iv"]
        flag = alice_flag["encrypted"]

        system(f"python3 utils/decrypt.py {ss} {iv} {flag}")


# part_one()
part_two()
