BASE_URL = "http://10.10.187.98"
USER = "guest"
SEPERATOR = ":"


def get_cookie(user_agent: str) -> str:
    session = requests.Session()
    session.get(BASE_URL, headers={"User-Agent": user_agent})
    cookie = session.cookies.get("secure_cookie")
    return urllib.parse.unquote(str(cookie))


def main():
    enc_secret_key = ""
    while True:
        ua_padding = 7 - (len(USER + SEPERATOR + SEPERATOR + enc_secret_key) % 8)
        ua = "A" * ua_padding
        prefix = USER + SEPERATOR + ua + SEPERATOR + enc_secret_key
        block_number = len(prefix) // 8
        cookie = get_cookie(ua)
        salt = cookie[:2]
        target_block = cookie[block_number * 13 : (block_number + 1) * 13]
        found = False
        for c in string.printable:
            test_string = prefix + c
            test_hash = crypt.crypt(test_string[-8:], salt)
            if test_hash == target_block:
                enc_secret_key += c
                found = True
                print(c, end="")
                break

        if not found:
            print(enc_secret_key)


main()
