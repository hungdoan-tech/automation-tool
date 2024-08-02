from abc import ABC
from typing import Generic, TypeVar, Callable, Collection

from src.common.BaseEnumeratedValidValue import BaseEnumeratedValidValue
from src.gui_2.global_state.DefinedType import Action

T = TypeVar('T', bound='BaseAction')


class BaseAction(BaseEnumeratedValidValue, Generic[T], ABC):
    _values: dict[str, T] = {}

    def __init__(self, code: str, description: str, created_version: str, invoke: Callable[[...], Action] = None):
        super().__init__(code, description, created_version)
        self.invoke: Callable[[str], Action] = invoke

    @classmethod
    def create(cls: type[T], code: str, description: str, created_version: str, action: Callable[[...], Action]) -> T:
        instance = cls(code, description, created_version, action)
        cls._values[code] = instance
        return instance

    @classmethod
    def get_values(cls: type[T]) -> Collection[T]:
        return cls._values.values()

    @classmethod
    def value_of(cls: type[T], code: str) -> T:
        return cls._values.get(code)
