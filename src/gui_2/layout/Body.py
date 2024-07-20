from src.gui_2.global_state_container.DefinedType import Action, States
from src.gui_2.global_state_container.action.TaskNameAction import TaskActionType
from src.gui_2.layout.RenderableComponent import RenderableComponent
from src.gui_2.layout.content.StandardTask import StandardTask
from src.gui_2.layout.content.TaskDropdown import TaskDropdown


class Body(RenderableComponent):

    def _initialize_state(self) -> dict[str,]:
        return {
            'task_name': '',
            'task': None
        }

    def _component_did_mount(self):
        pass

    def handle__global_state_change(self, action: Action, state: States) -> None:
        type = action.get('type')

        if type == TaskActionType.CHANGE_TASK_NAME:
            pass

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

        standard_task = StandardTask(master=self)
        standard_task.grid_configure(row=1, column=0, rowspan=9, columnspan=10, sticky='nsew')
        standard_task.render()
        pass
