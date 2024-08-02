from abc import ABC, abstractmethod

from src.gui_2.global_state.DefinedType import Action, States


class GlobalStateHandler(ABC):

    @abstractmethod
    def handle__global_state_change(self, action: Action, state: States) -> None:
        pass
