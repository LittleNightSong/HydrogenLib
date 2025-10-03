import hashlib


# module end


def calc_hash(string: bytes, hash_type: str = "sha256"):
    return getattr(hashlib, hash_type)(string)
