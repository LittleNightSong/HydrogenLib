from . import (
    aes,
    rsa
)


class BothCipher:
    def __init__(self, pubkey, prikey, iv=None):
        self.rsa_pubkey, self.rsa_prikey = pubkey, prikey
        self.aes_iv = iv

    def encrypt(self, plain_text: bytes):
        aes_key = aes.generate_key()
        encode_aes_key = rsa.encrypt(aes_key, self.rsa_pubkey)
        encrypted_data = aes.encrypt(plain_text, aes_key, self.aes_iv)
        return encrypted_data, encode_aes_key

    def decrypt(self, cipher_text: bytes, encoded_aes_key):
        aes_key = rsa.decrypt(encoded_aes_key, self.rsa_prikey)
        return aes.decrypt(cipher_text, aes_key, self.aes_iv)
