""""""

from typing import Any

from pydantic import BaseModel

from blufi.serial_number import SerialNumber


class BaseCommands(BaseModel):  # type: ignore[misc]
    """Base Commands"""

    cmd_type: int
    frame_control: int

    data_length: int
    sn: str = ""
    crc: str = ""

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        self.sn = SerialNumber().obj
        self.crc = "1236"
        assert len(self.crc) == 4


if __name__ == "__main__":
    bc = BaseCommands(cmd_type=1, frame_control=2, sn="12", data_length=2, crc="135")
    print(bc)
