import rsa


# module end

def generate_keys(size: int = 2048):
    """
    return pubkey, privkey
    """
    return rsa.newkeys(size)


def encrypt(plain_text: bytes, key: rsa.PublicKey):
    """
    return cipher_text
    """
    return rsa.encrypt(plain_text, key)


def decrypt(cipher_text: bytes, key: rsa.PrivateKey):
    """
    return plain_text
    """
    return rsa.decrypt(cipher_text, key)
