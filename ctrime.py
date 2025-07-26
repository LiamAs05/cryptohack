from utils.utils import ascii_to_hex
import string
import requests
from tqdm import tqdm

URL = lambda pt: f"https://aes.cryptohack.org/ctrime/encrypt/{pt}"

def send_pt(pt):
    return requests.get(URL(ascii_to_hex(pt))).json()["ciphertext"]

def main():
    # the script got stuck in the 'E' character, perhaps there were two minimal characters for the zlib compression
    # or an implementation error
    # anyway I completed this part by hand when I had 'CRIM'
    curr_pt = r"crypto{CRIME"
    curr_char = r" "
    curr_min_val = len(send_pt(curr_pt + curr_char))
    
    while True:
        for i in tqdm(string.printable):
            if len(send_pt(curr_pt + i)) < curr_min_val:
                curr_min_val = len(send_pt(curr_pt + i))
                curr_char = i
    
        curr_pt += curr_char
        print(curr_pt)
        if curr_char == '}':
            break
        curr_char = r" "
        curr_min_val = len(send_pt(curr_pt + curr_char))

if __name__ == "__main__":
    main()
