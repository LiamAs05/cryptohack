from utils.utils import PrintingSocket
import json
import base64
from tqdm import tqdm

ADDR = ('socket.cryptohack.org', 13370)
REQ = {"msg": "request"}

not_flag_bytes = []

for _ in range(20):
    not_flag_bytes.append(set())

set_to_diff = {i for i in range(256)}

with PrintingSocket() as s:
    s.connect(ADDR)
    s.recv_print()
    
    for _ in tqdm(range(2048)):
        s.send_dict(REQ)
        ct = json.loads(s.recv()).get("ciphertext", None)
        if ct:
            for i, b in enumerate(base64.b64decode(ct)):
                not_flag_bytes[i].add(b)
    
    for not_it in not_flag_bytes:
        diff = set_to_diff - not_it
        if len(diff) == 1:
            print(chr(diff.pop()), end="")
        else:
            print(set(map(chr, diff)), end="")
        