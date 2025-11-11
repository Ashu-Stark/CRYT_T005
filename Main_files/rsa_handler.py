import os
import random
import math
from rsa import rsa_encrypt, rsa_decrypt 

KEYFILE = "rsa_keys.txt"

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(n**0.5) + 1
    for i in range(3, r, 2):
        if n % i == 0:
            return False
    return True

def generate_prime(start=200, end=800):
    candidates = [p for p in range(start, end) if is_prime(p)]
    return random.choice(candidates)

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    return x % m

def generate_rsa_keypair():
    
    p = generate_prime(200, 500)
    q = generate_prime(500, 900)
    while q == p:
        q = generate_prime(500, 900)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if math.gcd(e, phi) != 1:
       
        for cand in range(3, phi, 2):
            if math.gcd(cand, phi) == 1:
                e = cand
                break

    d = modinv(e, phi)
    if d is None:
        raise Exception("Failed to compute modular inverse d")

    return {'p': p, 'q': q, 'n': n, 'e': e, 'd': d}

def save_rsa_keys(keys, filename=KEYFILE):
    
    with open(filename, "w") as f:
        f.write(f"{keys['p']},{keys['q']},{keys['n']},{keys['e']},{keys['d']}")

def load_rsa_keys(filename=KEYFILE):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        data = f.read().strip().split(",")
        if len(data) != 5:
            return None
        p, q, n, e, d = map(int, data)
        return {'p': p, 'q': q, 'n': n, 'e': e, 'd': d}

def ensure_rsa_keys():
    keys = load_rsa_keys()
    if keys is None:
        keys = generate_rsa_keypair()
        save_rsa_keys(keys)
    return keys

def rsa_encrypt_string(aes_key_str, e, n):
    return rsa_encrypt(aes_key_str, e, n)

def rsa_decrypt_list(cipher_list, d, n):
    return rsa_decrypt(cipher_list, d, n)
