import random
import string
from aes import aes_encrypt, aes_decrypt

KEY_LEN = 16

def generate_aes_key(length=KEY_LEN):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def encrypt_vote_with_aes(plaintext):
    
    key = generate_aes_key()
    enc = aes_encrypt(plaintext, key)
    return enc, key

def decrypt_vote_with_aes(encrypted_text, aes_key):
    return aes_decrypt(encrypted_text, aes_key)
