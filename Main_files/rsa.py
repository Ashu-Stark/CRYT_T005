def rsa_encrypt(msg, e, n):
    return [pow(ord(ch), e, n) for ch in msg]

def rsa_decrypt(cipher, d, n):
    return ''.join([chr(pow(c, d, n)) for c in cipher])


