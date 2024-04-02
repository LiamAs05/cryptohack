from json import dumps, loads

from utils.utils import PrintingSocket, hex_to_ascii

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13372))
    s.recv_print()
    s.send_print(dumps({"option": "get_flag"}).encode())
    f = loads(s.recv_print())["encrypted_flag"]
    s.send_print(dumps({"option": "encrypt_data", "input_data": f}).encode())
    print(hex_to_ascii(loads(s.recv_print())["encrypted_data"]))
