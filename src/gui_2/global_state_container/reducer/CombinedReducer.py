from src.gui_2.global_state_container.DefinedType import Reducer, States, Action


def combine_reducers(reducers: list[Reducer]):
    def combined_reducer(old_states: States = None, action: Action = None) -> States:

        if old_states is None:
            for reducer in reducers:
                old_states = reducer(None, action)

        new_states: States = {}
        for reducer in reducers:
            new_states = reducer(old_states, action)

        return new_states

    return combined_reducer
