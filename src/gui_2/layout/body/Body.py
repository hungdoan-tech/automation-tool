from tkinter import ttk

from src.gui_2.global_state.DefinedType import Action, States
from src.gui_2.global_state.GlobalStateHandler import GlobalStateHandler
from src.gui_2.global_state.action.TaskAction import TaskAction
from src.gui_2.layout.Component import Component
from src.task import TaskFactory
from src.task.AutomatedTask import AutomatedTask


class Body(Component, GlobalStateHandler):

    def _initialize_state(self) -> dict[str,]:
        self.__taskToVisibleInstance: dict[str, tuple[AutomatedTask, Component]] = {}
        return {
            'task_name': '',
            'task': None
        }

    def component_did_mount(self):
        pass

    def handle__global_state_change(self, action: Action, state: States) -> None:

        action_type: str = str(action.get('type'))

        if action_type == TaskAction.CHANGE_ACTIVE_TASK.get_code():

            active_task = str(action.get('payload'))

            if self.__taskToVisibleInstance.get(active_task) is None:
                settings: dict[str, str] = TaskFactory.get_task_settings(active_task)
                instance: AutomatedTask = TaskFactory.create_task_instance(active_task, settings, None)
                self.__taskToVisibleInstance[active_task] = (instance,)

    def render(self):
        col_num = 10
        runner = 0
        while runner < col_num:
            self.grid_rowconfigure(index=runner, weight=1)
            self.grid_columnconfigure(index=runner, weight=1)
            runner += 1

        notebook = ttk.Notebook(master=self)
        notebook.grid_configure(row=0, column=0, rowspan=10, columnspan=10, sticky='nswe')

        # Display welcome tab for the first time being displayed
        tab_1 = ttk.Frame(notebook)
        tab_1.columnconfigure(index=0, weight=1)
        tab_1.rowconfigure(index=0, weight=1)
        notebook.add(tab_1, text="Welcome")
