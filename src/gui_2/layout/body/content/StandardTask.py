from src.gui_2.layout.Component import Component


class StandardTask(Component):

    def _initialize_state(self) -> dict[str,]:
        return {'task_list': []}

    def component_did_mount(self):
        # self._set_state('field_name', )
        # mandatory_settings: list[str] = self.automated_task.mandatory_settings()
        # mandatory_settings.append('invoked_class')
        # mandatory_settings.append('time.unit.factor')
        # mandatory_settings.append('use.GUI')
        pass

    def render(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
