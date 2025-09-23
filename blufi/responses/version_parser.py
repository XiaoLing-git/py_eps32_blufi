""""""

from .parser import Parser


class VersionParser(Parser):
    """Version Parser"""

    def __init__(self, data: str) -> None:
        """init."""
        super().__init__(data)

    @property
    def major(self) -> int:
        """major"""
        return int.from_bytes(bytes.fromhex(self.content[:2]), byteorder="little")

    @property
    def minor(self) -> int:
        """minor"""
        return int.from_bytes(bytes.fromhex(self.content[2:4]), byteorder="little")

    @property
    def version(self) -> str:
        """version"""
        return f"V{self.major}.{self.minor}"

    def __str__(self) -> str:
        """str"""
        return f"{self.__class__.__name__}(" f"version={self.version}, " f"content={self.content})"
