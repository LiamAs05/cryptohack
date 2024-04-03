# https://en.wikipedia.org/wiki/Weak_key#Weak_keys_in_DES

# Specifically, there are six semi-weak key pairs, which obey:
# DES(K1, DES(K2, M)) = M
# We will examine one of these and encrypt the flag using the API:
# 3DES(K, FLAG) = C where K=K1K2 (concatenated)

# And then call 3DES(K, C) to get FLAG

from requests import get
from utils.utils import hex_to_ascii, get_flag_in_message

url = r"https://aes.cryptohack.org/triple_des/"

k1 = "E0FEE0FEF1FEF1FE"
k2 = "FEE0FEE0FEF1FEF1"
c = get(url+"encrypt_flag/"+k1+k2).json()["ciphertext"]
flag = get(url+"encrypt/"+k2+k1+"/"+c).json()["ciphertext"]
print(get_flag_in_message(hex_to_ascii(flag)))
