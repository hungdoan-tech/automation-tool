from src.gui_2.layout.RenderableComponent import RenderableComponent
from src.gui_2.layout.main_content.TaskDropdown import TaskDropdown


class Body(RenderableComponent):

    def _initialize_state(self) -> dict[str,]:
        return {
            'task_name': '',
            'task': None
        }

    def render(self):
        col_num = 10
        runner = 0
        while runner < col_num:
            self.grid_rowconfigure(index=runner, weight=1)
            self.grid_columnconfigure(index=runner, weight=1)
            runner += 1

        dropdown = TaskDropdown(master=self)
        dropdown.grid_configure(row=0, column=4, rowspan=1, columnspan=3, sticky='nsew')
        dropdown.render()
        pass
