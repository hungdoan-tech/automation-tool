from src.gui_2.state_container.Type import Reducer, States, Action


def combine_reducers(reducers: dict[str, Reducer]):
    def combined_reducer(old_state: States = None, action: Action = None) -> States:

        if old_state is None:
            for key, reducer in reducers.items():
                old_state[key] = reducer(None, action)

        new_state = {}
        for key, reducer in reducers.items():
            new_state[key] = reducer(old_state[key], action)

        return new_state

    return combined_reducer
