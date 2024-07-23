import tkinter as tk

from src.gui_2.global_state.DefinedType import Action, States
from src.gui_2.global_state.Store import Store
from src.gui_2.global_state.action.TaskAction import set_task_name, TaskAction
from src.gui_2.global_state.middleware.ErrorHandlingMiddleware import error_handling_middleware
from src.gui_2.global_state.middleware.LoggingMiddeware import logging_middleware
from src.gui_2.global_state.middleware.PromiseMiddleware import promise_middleware
from src.gui_2.global_state.reducer.CombinedReducer import combine_reducers
from src.gui_2.global_state.reducer.TaskReducer import task_name_reducer
from src.gui_2.layout.Component import Component

# Combine reducers
root_reducer = combine_reducers([task_name_reducer])

# Initial state
initial_state = {}

# Create the store
store = Store(initial_state, root_reducer, [error_handling_middleware, logging_middleware, promise_middleware])


class Test(Component):

    def _initialize_state(self) -> dict[str,]:
        return {"name": "Hung"}

    def render(self):
        self.label = tk.Label(master=self, text=self.state.get("name"), width=25, fg='#FFFFFF', bg='#00243D',
                              borderwidth=0)
        self.label.bind("<Button-1>", self.on_click)
        self.label.pack(side="left")
        TaskAction.CONVENTIONAL.action()

    def on_click(self, event):
        self.set_state({"name": "Khoa"})

    def handle_state_change(self, action: Action, state: States) -> None:
        print(f"Action dispatched: {action['type']}")
        print('New state:', state.get('task_name'))
        self.set_state({**self.state, "name": "Khoa"})

    def doSomething(self):
        unsubscribe = store.subscribe(self.handle_state_change)

        # Dispatch actions
        store.dispatch(set_task_name('John Doe'))

        unsubscribe()


if __name__ == '__main__':
    root = tk.Tk()
    instance = Test(master=root)
    instance.pack()
    root.mainloop()
    # time.sleep(3)
    # instance.doSomething()
