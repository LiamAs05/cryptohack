from utils.utils import PrintingSocket

AUTH = {"option": "authenticate", "password": ""}
RST_CONN = {"option": "reset_connection"}
RST_PASSW = {"option": "reset_password", "token": "00"*28}

with PrintingSocket() as s:
    s.connect(("socket.cryptohack.org", 13399))
    s.recv_print()
    data = ""
    while "flag" not in data:
        s.send_dict(AUTH)
        data = s.recv().decode()
        s.send_dict(RST_PASSW)
        s.recv()
        s.send_dict(RST_CONN)
        s.recv()
    print(data)
    