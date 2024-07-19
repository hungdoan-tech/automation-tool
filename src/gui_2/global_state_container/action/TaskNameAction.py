from enum import Enum


class TaskActionType(Enum):
    CHANGE_TASK_NAME = 'CHANGE_TASK_NAME'


def set_task_name(task_name: str):
    return {'type': TaskActionType.CHANGE_TASK_NAME, 'payload': task_name}
