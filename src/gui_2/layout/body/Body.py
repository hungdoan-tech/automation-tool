from tkinter import ttk

from src.gui_2.global_state.DefinedType import Action, States
from src.gui_2.global_state.GlobalStateHandler import GlobalStateHandler
from src.gui_2.global_state.Store import store
from src.gui_2.global_state.action.TaskAction import TaskAction
from src.gui_2.layout.Component import Component
from src.gui_2.layout.body.CloseableTab import CloseableTab
from src.task import TaskFactory
from src.task.AutomatedTask import AutomatedTask


class Body(Component, GlobalStateHandler):

    def _initialize_state(self) -> dict[str,]:

        states: dict[str,] = {'settings': input_setting_values}


    # If any change in Global State, body will be notified
    def component_did_mount(self):
        store.subscribe(self.handle__global_state_change)

    def handle__global_state_change(self, action: Action, state: States) -> None:

        action_type: str = str(action.get('type'))

        if action_type == TaskAction.CHANGE_ACTIVE_TASK.get_code():

            active_task = str(action.get('payload'))

            if self.__taskToVisibleInstance.get(active_task) is None:
                settings: dict[str, str] = TaskFactory.get_task_settings(active_task)
                instance: AutomatedTask = TaskFactory.create_task_instance(active_task, settings, None)

                # component
                self.__taskToVisibleInstance[active_task] = (instance,)
                self.set_state({**self.state,
                                'task_name': action['payload'],
                                'task': instance})

    def render(self):
        col_num = 10
        runner = 0
        while runner < col_num:
            self.grid_rowconfigure(index=runner, weight=1)
            self.grid_columnconfigure(index=runner, weight=1)
            runner += 1

        notebook = ttk.Notebook(master=self)
        notebook.grid_configure(row=0, column=0, rowspan=10, columnspan=10, sticky='nswe')

        current_settings: dict[str, str]  = self.state['setting']
        for current_setting in current_settings:

            # Display welcome tab for the first time being displayed
            tab_1 = CloseableTab(master=notebook, props={'task_name': })
            tab_1.columnconfigure(index=0, weight=1)
            tab_1.rowconfigure(index=0, weight=1)

        # tao instance closeabletab

        notebook.add(tab_1, text="Welcome")
