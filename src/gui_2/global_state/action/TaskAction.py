from typing import Callable, Dict, Collection, TypeVar, Generic, Type

from src.common.BaseEnumeratedValidValue import BaseEnumeratedValidValue
from src.gui_2.global_state.DefinedType import Action

# Define a TypeVar for the generic class
T = TypeVar('T', bound='TaskAction')


class TaskAction(BaseEnumeratedValidValue, Generic[T]):
    _values: Dict[str, T] = {}

    # Use TypeVar for class-level variables
    CONVENTIONAL: T
    INTEREST_ONLY: T

    def __init__(self, code: str, description: str, created_version: str, invoke: Callable[[str], Action] = None):
        super().__init__(code, description, created_version)
        self.invoke: Callable[[str], Action] = invoke

    @classmethod
    def create(cls: Type[T], code: str, description: str, created_version: str, action: Callable[[str], Action]) -> T:
        instance = cls(code, description, created_version, action)
        cls._values[code] = instance
        return instance

    @classmethod
    def get_values(cls: Type[T]) -> Collection[T]:
        return cls._values.values()

    @classmethod
    def value_of(cls: Type[T], code: str) -> T:
        return cls._values.get(code)


# Example implementation of Action (adjust as needed)
def set_task_name(task_name: str) -> Action:
    return {'type': TaskAction.CONVENTIONAL.get_code(), 'payload': task_name}


# Initialize constants using class method for proper typing
TaskAction.CONVENTIONAL = TaskAction.create("C", "Conventional", "6.5", set_task_name)
TaskAction.INTEREST_ONLY = TaskAction.create("I", "Interest Only", "6.5", lambda x: {'type': 'I', 'payload': x})

# Example usage
if __name__ == "__main__":
    TaskAction.CONVENTIONAL.invoke()
