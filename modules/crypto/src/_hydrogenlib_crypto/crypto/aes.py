import os
from enum import Enum

import pyaes

from .methods import split, pad, unpad


def generate_key(size: int = 16):
    return os.urandom(size)


def generate_iv(size: int = 16):
    return os.urandom(size)


def generate(size: int = 16):
    return generate_key(size), generate_iv(size)


def split_and_pad(text: bytes, size: int = 16):
    return [pad(i, size) for i in split(text, size)]


def bytes_join(args):
    return b''.join(args)


class AESMode(Enum):
    CBC = pyaes.AESModeOfOperationCBC
    ECB = pyaes.AESModeOfOperationECB
    CFB = pyaes.AESModeOfOperationCFB
    OFB = pyaes.AESModeOfOperationOFB
    CTR = pyaes.AESModeOfOperationCTR


class Aes:
    @property
    def key(self):
        return self._key

    @property
    def iv(self):
        return self._iv

    @key.setter
    def key(self, key):
        self._key = key
        self._generate_aes_object()

    @iv.setter
    def iv(self, iv):
        self._iv = iv
        self._generate_aes_object()

    def _generate_aes_object(self):
        self._aes = self._type.value(self.key, self.iv)

    def __init__(self, key, iv, type=AESMode.CBC):
        self._key = key
        self._iv = iv
        self._type = type
        self._aes = None

        self._generate_aes_object()

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        解密
        :param ciphertext: 原始密文
        :return: bytes
        """
        ciphertext_list = split(ciphertext)
        plaintext_list = [self._aes.decrypt(i) for i in ciphertext_list]

        if plaintext_list:
            plaintext_list[-1] = unpad(plaintext_list[-1])

        return bytes_join(plaintext_list)

    def encrypt(self, text: bytes):
        """
        加密
        :param text: 明文
        :return: bytes
        """
        plaintext_list = split_and_pad(text)
        cipertext_list = [self._aes.encrypt(i) for i in plaintext_list]

        return bytes_join(cipertext_list)
