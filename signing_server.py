from utils.utils import PrintingSocket, get_flag_in_message, hex_to_ascii

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13374))
    s.recv_print()
    s.send_print_dict({"option": "get_secret"})
    res = s.recv_print_dict()
    secret = res["secret"]
    s.send_print_dict({"option": "sign", "msg": secret})
    res = s.recv_print_dict()["signature"]
    print(f"FLAG: {get_flag_in_message(hex_to_ascii(res))}")
