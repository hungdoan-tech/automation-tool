import tkinter as tk
from typing import Callable

from src.gui_2.layout.Component import Component


class Field(Component):

    def __init__(self, master, props: dict[str,] = None, *args, **kwargs):
        super().__init__(master, props, *args, **kwargs)

    def render(self):

        setting_key = self.props['setting_key']
        setting_value = self.props['setting_value']

        setting_key_in_lowercase: str = setting_key.lower()

        if setting_key_in_lowercase.endswith('invoked_class'):
            return None

        if setting_key_in_lowercase.startswith('use.'):
            return self.create_checkbox_input(setting_key, setting_value)

        if setting_key_in_lowercase.endswith('.folder'):
            return self.create_folder_path_input(setting_key, setting_value)

        if setting_key_in_lowercase.endswith('.path'):
            return self.create_file_path_input(setting_key, setting_value)

        # default case, just text field
        return self.create_textbox_input(setting_key, setting_value)


    def create_checkbox_input(self, setting_key: str, setting_value: str) -> tk.Checkbutton:

        is_gui: bool = True if setting_value.lower() == 'true' else False

        is_checked = tk.BooleanVar(value=is_gui)

        field_change_callback: Callable = self.props['field_change_callback']

        use_gui_checkbox = tk.Checkbutton(self.master, text=setting_key, background='#2FACE8',
                                          width=21, height=1,
                                          variable=is_checked,
                                          command=lambda: field_change_callback(setting_key, str(is_checked)))
        use_gui_checkbox.pack(anchor="w", pady=5)

        return use_gui_checkbox