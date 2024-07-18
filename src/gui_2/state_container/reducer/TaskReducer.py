from src.gui_2.state_container.Type import States, Action, New_State_Value


def task_name_reducer(state: States = None, action: Action = None) -> New_State_Value:
    if state is None:
        state = {'task_name': None}

    match action['type']:
        case 'SET_TASK_NAME':
            return action['payload']

    return state
