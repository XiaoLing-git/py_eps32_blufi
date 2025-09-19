""""""

from __future__ import annotations


class SerialNumber:
    """ """

    _instance = None

    def __new__(cls) -> SerialNumber:
        """__new__"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.serial_number = -1  # type: ignore[has-type]
        return cls._instance

    @property
    def obj(self) -> str:
        """obj"""
        self.serial_number = self.serial_number + 1  # type: ignore[has-type]
        self.serial_number = self.serial_number & 0xFF
        print(int.to_bytes(self.serial_number, byteorder="little", length=1).hex())
        return int.to_bytes(self.serial_number, byteorder="little", length=1).hex()
