from json import dumps, loads
from os import system
from time import sleep

from utils.utils import PrintingSocket

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13371))
    s.recv_print()
    data = loads(s.recv_print().decode().split("Send")[0])
    alice_A = data["A"]
    p = data["p"]
    g = data["g"]

    # If we send B=1, Alice will calculate her private key as 1**a = 1
    data["A"] = "0x1"
    s.send_print(dumps(data).encode())
    s.recv_print()
    data = loads(s.recv_print().decode().split("Send")[0])
    data["B"] = "0x1"
    s.send_print(dumps(data).encode())
    sleep(2)  # Waiting for encryption of AES key
    d = loads(s.recv_print().decode().split("Alice: ")[1])

    iv = d["iv"]
    e_flag = d["encrypted_flag"]
    system(f"python3 utils/decrypt.py 1 {iv} {e_flag}")
