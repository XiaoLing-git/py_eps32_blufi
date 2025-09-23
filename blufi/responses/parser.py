""""""


class Parser:
    """base parser"""

    __slots__ = ("__content",)

    def __init__(self, data: str) -> None:
        """init."""
        self.__content = data

    @property
    def content(self) -> str:
        """content"""
        return self.__content

    def __str__(self) -> str:
        """str"""
        return f"{self.__class__.__name__}(content={self.content})"


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
