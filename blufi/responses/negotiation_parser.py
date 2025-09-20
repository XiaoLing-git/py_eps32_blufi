""""""


class NegotiationParser:
    """NegotiationParser Parser"""

    def __init__(self, data: str, data_length: int) -> None:
        """init."""
        self.__content = data
        self.__data_length = data_length
        assert len(self.content) == (2 * self.__data_length)

    @property
    def content(self) -> str:
        """content"""
        return self.__content
