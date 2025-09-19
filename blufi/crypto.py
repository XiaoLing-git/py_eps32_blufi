""""""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh

DH_P = (
    "0xcf5cf5c38419a724957ff5dd323b9c45c3cdd261eb740f69aa94b8bb1a5c9640"
    + "9153bd76b24222d03274e4725a5406092e9e82e9135c643cae98132b0d95f7d6"
    + "5347c68afc1e677da90e51bbab5f5cf429c291b4ba39c6b2dc5e8c7231e46aa7"
    + "728e87664532cdf547be20c9a3fa8342be6e34371a27c06f7dc0edddd2f86373"
)


# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/
class BlufiCrypto:
    """"""

    def __init__(self) -> None:
        """"""
        self.p = int(DH_P, 0)
        self.g = 2
        self.y = 0
        self.private_Key = None
        self.public_Key = None

    def genKeys(self) -> None:
        """"""
        pn = dh.DHParameterNumbers(self.p, self.g)
        parameters = pn.parameters()
        self.private_Key = parameters.generate_private_key()
        assert self.private_Key is not None
        self.public_Key = self.private_Key.public_key()
        assert self.public_Key is not None
        self.y = self.public_Key.public_numbers().y

    def deriveSharedKey(self, peer_pub_bytes: bytes) -> bytes:
        """"""
        pn = dh.DHParameterNumbers(self.p, self.g)
        y = int.from_bytes(peer_pub_bytes, "big")
        peer_public_numbers = dh.DHPublicNumbers(y, pn)
        peer_public_key = peer_public_numbers.public_key()
        assert self.private_Key is not None
        shared_key = self.private_Key.exchange(peer_public_key)
        digest = hashes.Hash(hashes.MD5())
        digest.update(shared_key)
        return digest.finalize()

    def getPBytes(self) -> bytes:
        """"""
        return bytes.fromhex(DH_P[2:])

    def getGBytes(self) -> bytes:
        """"""
        return bytes.fromhex("02")

    def getYBytes(self) -> bytes:
        """"""
        pub_bytes = self.y.to_bytes(2048 // 8, "big")
        return pub_bytes
