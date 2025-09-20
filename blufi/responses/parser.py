""""""


class Parser:
    """base parser"""

    def __init__(self, data: str) -> None:
        """init."""
        self.__content = data

    @property
    def content(self) -> str:
        """content"""
        return self.__content
