import tkinter as tk

from src.gui_2.global_state_container.DefinedType import Action, States
from src.gui_2.global_state_container.Store import Store
from src.gui_2.global_state_container.action.TaskNameAction import set_task_name
from src.gui_2.global_state_container.reducer.CombinedReducer import combine_reducers
from src.gui_2.global_state_container.reducer.TaskReducer import task_name_reducer
from src.gui_2.layout.RenderableComponent import RenderableComponent

# Combine reducers
root_reducer = combine_reducers([task_name_reducer])

# Initial state
initial_state = {}

# Create the store
store = Store(initial_state, root_reducer)


class Test(RenderableComponent):

    def render(self):
        pass

    def handle_state_change(self, action: Action, state: States) -> None:
        print(f"Action dispatched: {action['type']}")
        print('New state:', state.get('task_name'))

    def doSomething(self):
        unsubscribe = store.subscribe(self.handle_state_change)

        # Dispatch actions
        store.dispatch(set_task_name('John Doe'))

        unsubscribe()


if __name__ == '__main__':
    root = tk.Tk()
    instance = Test(master=root)
    instance.doSomething()
