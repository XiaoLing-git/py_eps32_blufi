""""""

from typing import Any

from pydantic import BaseModel

from blufi.errors import GenerateCommandException
from blufi.models.base_models import ControlAddress, DataAddress, TypeField
from blufi.serial_number import SerialNumber


class PocketType(BaseModel):  # type: ignore[misc]
    """Pocket Type"""

    type_field: TypeField
    func_code: ControlAddress | DataAddress

    def model_post_init(self, context: Any, /) -> None:
        """model post init"""
        if self.type_field is TypeField.Control:
            if not isinstance(self.func_code, ControlAddress):
                raise GenerateCommandException(f"{self.func_code} is not {ControlAddress}")
        if self.type_field is TypeField.Data:
            if not isinstance(self.func_code, DataAddress):
                raise GenerateCommandException(f"{self.func_code} is not {DataAddress}")

    def hex(self) -> str:
        """hex to str"""
        value = self.type_field.value | self.func_code.value
        return f"{value:02X}"


class BaseCommands(BaseModel):  # type: ignore[misc]
    """Base Commands"""

    pocket_type: PocketType
    frame_control: int

    data_length: int | None = None
    sn: str | None = None
    crc: str | None = None

    def model_post_init(self, context: Any, /) -> None:
        """model_post_init"""
        print(self.pocket_type)
        self.sn = SerialNumber().obj
        self.crc = "1236"
        assert len(self.crc) == 4


if __name__ == "__main__":

    bc = BaseCommands(
        pocket_type=PocketType(type_field=TypeField.Data, func_code=DataAddress.STA_WIFI_BSSID),
        frame_control=2,
        sn="12",
        data_length=2,
        crc="135",
    )
    print(bc)
