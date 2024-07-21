from tkinter.ttk import Combobox

from src.common.util.FileUtil import get_all_concrete_task_names
from src.gui_2.global_state.Store import store
from src.gui_2.global_state.action.TaskNameAction import set_task_name
from src.gui_2.layout.Component import Component


class TaskDropdown(Component):

    def __init__(self, master, props: dict[str,] = None, *args, **kwargs):
        super().__init__(master, props, *args, **kwargs)
        self.tasks_dropdown: Combobox = None

    def _initialize_state(self) -> dict[str,]:
        return {'task_list': []}

    def render(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        self.tasks_dropdown: Combobox = Combobox(master=self, state="readonly", width=110, height=20,
                                                 background='#FB3D52', foreground='#FFFFFF')
        self.tasks_dropdown.grid_configure(row=0, column=0)
        self.tasks_dropdown.bind("<<ComboboxSelected>>", self.handle_tasks_dropdown)
        self.tasks_dropdown['values'] = self.state.get('task_list')

    def handle_tasks_dropdown(self, event):
        selected_task = event.widget.get()
        store.dispatch(set_task_name(selected_task))

    def component_did_mount(self):
        self.set_state({'task_list': get_all_concrete_task_names()})
        self.tasks_dropdown.focus_set()
        self.tasks_dropdown.current(0)
        self.tasks_dropdown.event_generate("<<ComboboxSelected>>")
