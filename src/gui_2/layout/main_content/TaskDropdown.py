from tkinter.ttk import Combobox

from src.common.FileUtil import get_all_concrete_task_names
from src.gui_2.layout.RenderableComponent import RenderableComponent


class TaskDropdown(RenderableComponent):

    def _initialize_state(self) -> dict[str,]:
        return {'task_list': []}

    def component_did_mount(self):
        self.set_state({'task_list': get_all_concrete_task_names()})

    def render(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        tasks_dropdown: Combobox = Combobox(master=self, state="readonly", width=110, height=20,
                                            background='#FB3D52', foreground='#FFFFFF')
        tasks_dropdown.grid_configure(row=0, column=0)
        # tasks_dropdown.bind("<<ComboboxSelected>>", self.handle_tasks_dropdown)
        tasks_dropdown['values'] = self.state.get('task_list')
