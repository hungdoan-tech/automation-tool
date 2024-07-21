from enum import Enum

from src.gui_2.global_state.DefinedType import Action


class TaskActionType(Enum):
    CHANGE_TASK_NAME = 'CHANGE_TASK_NAME'


def set_task_name(task_name: str) -> Action:
    return {'type': TaskActionType.CHANGE_TASK_NAME, 'payload': task_name}
