from Crypto.PublicKey import RSA
from requests import get

t = get(
    "https://cryptohack.org/static/challenges/privacy_enhanced_mail_1f696c053d76a78c2c531bb013a92d4a.pem"
)
print(RSA.importKey(t.text).d)
