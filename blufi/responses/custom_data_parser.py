""""""

import json

from .parser import Parser


class CustomDataParser(Parser):
    """Custom Data Parser"""

    def __init__(self, data: str) -> None:
        """init."""
        super().__init__(data)

    @property
    def content(self) -> str:
        """content"""
        return bytes.fromhex(super().content).decode()

    @property
    def format(self) -> list[dict[str, str | int]]:
        """format"""
        result = []
        if "}," in self.content:
            content = self.content[1:-1].replace("},", "}")
            for i in content.split("}"):
                try:
                    temp = json.loads(i + "}")
                    result.append(temp)
                except Exception as e:
                    print(e)
        else:
            result.append(self.content)
        return result

    def __str__(self) -> str:
        """str"""
        return f"{self.__class__.__name__}(content={self.format})"
