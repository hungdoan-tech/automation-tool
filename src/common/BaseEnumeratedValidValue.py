from abc import ABC


class BaseEnumeratedValidValue(ABC):
    def __init__(self, code: str, description: str, created_version: str = None):
        self._code = code
        self._description = description
        self._created_version = created_version

    def get_code(self) -> str:
        return self._code

    def get_description(self) -> str:
        return self._description

    def get_created_version(self) -> str:
        return self._created_version

    def __eq__(self, other) -> bool:
        if isinstance(other, BaseEnumeratedValidValue):
            return self._code == other._code
        return False

    def __hash__(self) -> int:
        return hash(self._code)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{{{self._code}={self._description}}}"
