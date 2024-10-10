from src.gui_2.global_state.DefinedType import States, Action
from src.gui_2.global_state.action.TaskAction import TaskAction


def task_name_reducer(states: States = None, action: Action = None) -> States:
    if states is None:
        states = {'task_name': None}

    action_type: str = action['type']

    if action_type == TaskAction.CHANGE_ACTIVE_TASK.get_code():
        return {**states, 'task_name': action['payload']}


    return states
