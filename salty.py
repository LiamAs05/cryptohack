from Crypto.Util.number import long_to_bytes

# C is encrypted with e=1 and c doesn't wrap around N (c < N)
# So c is not actually encrypted
c = 44981230718212183604274785925793145442655465025264554046028251311164494127485

print(long_to_bytes(c).decode())
