""""""

from typing import Any

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.utils import Buffer


# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.algorithms.AES
class BlufiAES(object):
    """AES/CFB/NoPadding"""

    __slots__ = (
        "key",
        "iv",
        "cipher",
        "encryptor",
        "decryptor",
    )

    def __init__(self, key: Buffer, iv: Buffer) -> None:
        """"""
        self.key = key
        self.iv = iv
        self.cipher = Cipher(algorithms.AES128(self.key), modes.CFB(self.iv))
        self.encryptor = self.cipher.encryptor()
        self.decryptor = self.cipher.decryptor()

    def encrypt(self, data: Buffer) -> Any:
        """"""
        ct = self.encryptor.update(data) + self.encryptor.finalize()
        return ct

    def decrypt(self, data: Buffer) -> Any:
        """"""
        pt = self.decryptor.update(data) + self.decryptor.finalize()
        return pt
