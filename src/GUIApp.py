import threading
import tkinter as tk
from tkinter import Label, Frame, Text
from tkinter.ttk import Combobox
import os
import importlib
from logging import Logger
from types import ModuleType

from src.AutomatedTask import AutomatedTask
from src.Constants import ROOT_DIR
from src.FileUtil import load_key_value_from_file_properties
from src.ResourceLock import ResourceLock
from src.ThreadLocalLogger import get_current_logger


class GUIApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Automation Tool")
        self.geometry('800x600')

        self.logger: Logger = get_current_logger()

        self.container_frame = tk.Frame(self)
        self.container_frame.pack()

        self.myLabel = Label(self.container_frame, text='Automation Tool', font=('Maersk Headline Bold', 16))
        self.myLabel.pack()

        self.automated_tasks_dropdown = Combobox(
            master=self.container_frame,
            state="readonly",
        )
        self.automated_tasks_dropdown.pack()

        self.content_frame = Frame(self.container_frame, width=500, height=300, bd=1, relief=tk.SOLID)
        self.content_frame.pack(padx=20, pady=20)

        self.automated_tasks_dropdown.bind("<<ComboboxSelected>>", self.on_selection_change)

        self.populate_dropdown()

        self.current_input_setting_values = {}
        self.current_automated_task_name = None

    def populate_dropdown(self):
        input_dir: str = os.path.join(ROOT_DIR, "input")
        automated_task_names: list[str] = []

        with ResourceLock(file_path=input_dir):
            for dir_name in os.listdir(input_dir):
                if dir_name.lower().endswith(".properties"):
                    automated_task_names.append(dir_name.replace(".properties", ""))

        automated_task_names.remove("InvokedClasses")
        self.automated_tasks_dropdown['values'] = automated_task_names

    def on_selection_change(self, event):
        self.persist_settings_to_file()
        selected_task = self.automated_tasks_dropdown.get()
        self.update_frame_content(selected_task)

    def update_frame_content(self, selected_task):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create new content based on the selected task
        self.logger.info('Display fields for task {}'.format(selected_task))

        clazz_module: ModuleType = importlib.import_module('src.' + selected_task)
        clazz = getattr(clazz_module, selected_task)

        setting_file = os.path.join(ROOT_DIR, 'input', '{}.properties'.format(selected_task))
        input_setting_values: dict[str, str] = load_key_value_from_file_properties(setting_file)
        input_setting_values['invoked_class'] = selected_task
        input_setting_values['use.GUI'] = 'True'
        input_setting_values['time.unit.factor'] = '1'

        self.current_input_setting_values = input_setting_values
        self.current_automated_task_name = selected_task

        automated_task: AutomatedTask = clazz(input_setting_values)

        for each_setting in input_setting_values:
            # Create a container frame for each label and text input pair
            setting_frame = Frame(self.content_frame)
            setting_frame.pack(anchor="w", pady=5)

            # Create the label and text input widgets inside the container frame
            field_label = Label(master=setting_frame, text=each_setting, width=15)
            field_label.pack(side="left")

            field_input = Text(master=setting_frame, width=30, height=1)
            field_input.pack(side="left")

            field_input.special_id = each_setting
            field_input.insert("1.0", input_setting_values[each_setting])
            field_input.bind("<KeyRelease>", self.update_field_data)

        perform_button = tk.Button(self.content_frame, text='Perform', font=('Maersk Headline Bold', 10),
                                   command=lambda: self.perform_task(automated_task))
        perform_button.pack()

    def perform_task(self, task: AutomatedTask):
        # threading.Thread(target=task.perform,
        #                  daemon=False)
        task.perform()

    def update_field_data(self, event):
        logger: Logger = get_current_logger()
        text_widget = event.widget
        new_value = text_widget.get("1.0", "end-1c")
        field_name = text_widget.special_id
        self.current_input_setting_values[field_name] = new_value
        logger.info("Change data on field {} to {}".format(field_name, new_value))

    def persist_settings_to_file(self):
        if self.current_automated_task_name is None:
            return

        logger: Logger = get_current_logger()
        file_path: str = os.path.join(ROOT_DIR, "input", "{}.properties".format(self.current_automated_task_name))
        logger.info("Try to persist data to {}".format(file_path))

        with ResourceLock(file_path=file_path):

            with open(file_path, 'w') as file:
                file.truncate(0)

            with open(file_path, 'a') as file:
                for key, value in self.current_input_setting_values.items():
                    file.write(f"{key} = {value}\n")


if __name__ == "__main__":
    app = GUIApp()
    app.mainloop()
