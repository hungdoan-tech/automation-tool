from src.gui_2.global_state.DefinedType import Action
from src.gui_2.global_state.action.BaseAction import BaseAction

BIND_NAME: str = 'TaskAction'


class TaskAction(BaseAction[BIND_NAME]):
    CHANGE_ACTIVE_TASK: BIND_NAME

    INTEREST_ONLY: BIND_NAME


def __set_task_name(task_name: str) -> Action:
    return {'type': TaskAction.CHANGE_ACTIVE_TASK.get_code(), 'payload': task_name}


TaskAction.CHANGE_ACTIVE_TASK = TaskAction.create("C", "Conventional", "6.5", __set_task_name)
TaskAction.INTEREST_ONLY = TaskAction.create("I", "Interest Only", "6.5", lambda x: {'type': 'I', 'payload': x})
