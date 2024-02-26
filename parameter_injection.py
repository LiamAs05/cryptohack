from json import dumps, loads
from os import system
from socket import socket
from time import sleep


def recv_print(s):
    t = s.recv(4096)
    print(t.decode())
    return t


def send_print(s, data: bytes):
    print(data.decode())
    s.send(data)


with socket() as s:
    s.connect(("socket.cryptohack.org", 13371))
    recv_print(s)
    data = loads(recv_print(s).decode().split("Send")[0])
    alice_A = data["A"]
    p = data["p"]
    g = data["g"]

    # If we send B=1, Alice will calculate her private key as 1**a = 1
    data["A"] = "0x1"
    send_print(s, dumps(data).encode())
    recv_print(s)
    data = loads(recv_print(s).decode().split("Send")[0])
    data["B"] = "0x1"
    send_print(s, dumps(data).encode())
    sleep(2)  # Waiting for encryption of AES key
    d = loads(recv_print(s).decode().split("Alice: ")[1])

    iv = d["iv"]
    e_flag = d["encrypted_flag"]
    system(f"python3 utils/decrypt.py 1 {iv} {e_flag}")
