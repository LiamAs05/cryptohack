from Crypto.Util.number import bytes_to_long
from sympy import factorint

from utils.utils import PrintingSocket, get_flag_in_message, num_to_hexstr

s = bytes_to_long(b"admin=True")
p, q = factorint(s).keys()

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13376))
    s.recv_print()
    s.send_print_dict({"option": "get_pubkey"})
    N, e = s.recv_print_dict().values()
    N = int(N, 16)
    s.send_print_dict({"option": "sign", "msg": num_to_hexstr(p)})
    pe = s.recv_print_dict()["signature"][2:]
    s.send_print_dict({"option": "sign", "msg": num_to_hexstr(q)})
    qe = s.recv_print_dict()["signature"][2:]
    res = hex(int(pe, 16) * int(qe, 16) % N)[2:]
    s.send_print_dict(
        {
            "option": "verify",
            "msg": bytes.hex(b"admin=True"),
            "signature": res,
        },
    )
    res = s.recv_print_dict()["response"]
    print(f"FLAG: {get_flag_in_message(res)}")
