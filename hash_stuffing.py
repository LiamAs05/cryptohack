from utils.utils import PrintingSocket
from json import dumps

BLOCK_SIZE = 32


def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len] * padding_len)


data = dumps({"m1": "01", "m2": "01" + "1f" * 31}).encode()

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13405))
    s.recv_print()
    s.send_print(data)
    print(s.recv_print()
