""""""


class Parser:
    """base parser"""

    def __init__(self, data: str) -> None:
        """init."""
        self.__content = data
        # assert len(self.content) == 2

    @property
    def content(self) -> str:
        """content"""
        return self.__content


class DebugParser:
    """Debug Parser"""

    def __init__(self, data: str) -> None:
        """init."""
        self.__content = data
        print(f"{self.__class__.__name__} {data}")

    @property
    def content(self) -> str:
        """content"""
        return self.__content
