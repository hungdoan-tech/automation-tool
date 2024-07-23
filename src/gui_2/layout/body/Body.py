from tkinter import ttk

from src.gui_2.global_state.DefinedType import Action, States
from src.gui_2.layout.Component import Component


class Body(Component):

    def _initialize_state(self) -> dict[str,]:
        return {
            'task_name': '',
            'task': None
        }

    def component_did_mount(self):
        pass

    def handle__global_state_change(self, action: Action, state: States) -> None:
        type = action.get('type')

    def render(self):
        col_num = 10
        runner = 0
        while runner < col_num:
            self.grid_rowconfigure(index=runner, weight=1)
            self.grid_columnconfigure(index=runner, weight=1)
            runner += 1

        notebook = ttk.Notebook(master=self)
        notebook.grid_configure(row=0, column=0, rowspan=10, columnspan=10, sticky='nswe')

        # Tab #1
        tab_1 = ttk.Frame(notebook)
        tab_1.columnconfigure(index=0, weight=1)
        tab_1.rowconfigure(index=0, weight=1)
        notebook.add(tab_1, text="Tab 1")
