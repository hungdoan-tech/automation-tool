from src.gui_2.global_state.DefinedType import States, Action
from src.gui_2.global_state.action.TaskNameAction import TaskActionType


def task_name_reducer(states: States = None, action: Action = None) -> States:
    if states is None:
        states = {'task_name': None}

    match action['type']:

        case TaskActionType.CHANGE_TASK_NAME:
            return {**states, 'task_name': action['payload']}

    return states
