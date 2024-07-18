from src.gui_2.state_container.Store import Store
from src.gui_2.state_container.Type import Action, States
from src.gui_2.state_container.action.TaskNameAction import set_task_name
from src.gui_2.state_container.reducer.CombinedReducer import combine_reducers
from src.gui_2.state_container.reducer.TaskReducer import task_name_reducer

# Combine reducers
root_reducer = combine_reducers({
    'task_name': task_name_reducer
})

# Initial state
initial_state = {
    'task_name': 'hung',
}

# Create the store
store = Store(initial_state, root_reducer)


# Subscribe to state changes
def handle_state_change(action: Action, state: States) -> None:
    print(f"Action dispatched: {action['type']}")
    print('New state:', state.get('task_name'))


unsubscribe = store.subscribe(handle_state_change)

# Dispatch actions
store.dispatch(set_task_name('John Doe'))

unsubscribe()
