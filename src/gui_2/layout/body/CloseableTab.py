import os

from src.common.util.FileUtil import load_key_value_from_file_properties, persist_settings_to_file
from src.gui_2.layout.Component import Component
from src.gui_2.layout.body.Field import Field
from src.setup.packaging.path.PathResolvingService import PathResolvingService

class CloseableTab(Component):
    def __init__(self, master, props: dict[str,] = None, *args, **kwargs):
        super().__init__(master, props, *args, **kwargs)

    def _initialize_state(self) -> dict[str,]:

        current_task_name = self.props['task_name']

        setting_file = os.path.join(PathResolvingService.get_instance().get_input_dir(),
                                    '{}.properties'.format(current_task_name))

        input_setting_values: dict[str, str] = load_key_value_from_file_properties(setting_file)
        input_setting_values['invoked_class'] = current_task_name

        if input_setting_values.get('time.unit.factor') is None:
            input_setting_values['time.unit.factor'] = '1'

        if input_setting_values.get('use.GUI') is None:
            input_setting_values['use.GUI'] = 'True'

        states: dict[str,] = {'settings': input_setting_values}
        return states

    def render(self):
        current_settings: dict[str, str] = self.state['setting']

        for setting_key, setting_value in current_settings.items():
            field = Field(master=self, props={'field_change_callback': self.field_change_callback,
                                              'setting_key': setting_key,
                                              'setting_value': setting_value
                                              })

        # button
        # field
        # logging_box
        # progress_bar

        pass

    def field_change_callback(self, setting_key: str, setting_value: str):

        self.state['setting'][setting_key] = setting_value
        persist_settings_to_file(self.props['task_name'], self.state['settings'])

