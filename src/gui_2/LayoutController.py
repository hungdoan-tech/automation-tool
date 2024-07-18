from src.common.FileUtil import get_all_concrete_task_names, load_key_value_from_file_properties, \
    persist_settings_to_file
from src.gui.UIComponentFactory import UIComponentFactory
from src.setup.packaging.path.PathResolvingService import PathResolvingService
import os
import tkinter as tk
from tkinter import Label, Frame, messagebox, Button
from tkinter.ttk import Combobox


class LayoutController():

    def __init__(self, root, task_manager, logger_setup_callback):
        self.root = root
        self.task_manager = task_manager
        self.logger_setup_callback = logger_setup_callback
        self.frames = {}
        self.current_task_name = None

    def render(self):
        self.root.title("Automation Tool")
        self.root.geometry('1080x980')
        self.root.configure(bg="#FFFFFF")

        whole_app_frame = tk.Frame(self.root, bg="#FFFFFF")
        whole_app_frame.pack()

        resource_dir = PathResolvingService.get_instance().resolve('resource')
        logo_image: tk.PhotoImage = tk.PhotoImage(file=os.path.join(resource_dir, "img", "logo.png"))

        self.render_header(parent_frame=whole_app_frame, logo=logo_image)

        tasks_dropdown: Combobox = self.render_tasks_dropdown(parent_frame=whole_app_frame)

        self.main_content_frame = Frame(master=whole_app_frame, width=1080, height=600, bd=1, relief=tk.SOLID,
                                        bg='#FFFFFF', borderwidth=0)
        self.main_content_frame.pack(padx=10, pady=10)

        self.render_main_content_frame_for_first_task(tasks_dropdown=tasks_dropdown)

        self.progress_bar, self.progress_bar_label = self.render_progress_bar(parent_frame=whole_app_frame)

        self.logging_textbox = self.render_textbox_logger(parent_frame=whole_app_frame)

    def render_header(self, parent_frame: Frame, logo: tk.PhotoImage) -> Label:
        logo_label: Label = Label(parent_frame, bg="#FFFFFF", width=980, image=logo, compound=tk.CENTER)
        logo_label.pack()
        return logo_label

    def render_tasks_dropdown(self, parent_frame: Frame) -> Combobox:
        tasks_dropdown: Combobox = Combobox(master=parent_frame, state="readonly", width=110, height=20,
                                            background='#FB3D52', foreground='#FFFFFF')
        tasks_dropdown.pack(padx=10, pady=10)
        tasks_dropdown.bind("<<ComboboxSelected>>", self.handle_tasks_dropdown)
        tasks_dropdown['values'] = get_all_concrete_task_names()
        return tasks_dropdown

    def render_main_content_frame(self, selected_task):
        # Clear the content frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # Create new content based on the selected task
        setting_file = os.path.join(PathResolvingService.get_instance().get_input_dir(),
                                    '{}.properties'.format(selected_task))
        if not os.path.exists(setting_file):
            with open(setting_file, 'w'):
                pass  # File created, do nothing

        input_setting_values: dict[str, str] = load_key_value_from_file_properties(setting_file)
        input_setting_values['invoked_class'] = selected_task

        if input_setting_values.get('time.unit.factor') is None:
            input_setting_values['time.unit.factor'] = '1'

        if input_setting_values.get('use.GUI') is None:
            input_setting_values['use.GUI'] = 'True'

        automated_task = self.task_manager.get_task_instance(selected_task, input_setting_values,
                                                             self.logger_setup_callback)
        mandatory_settings: list[str] = automated_task.mandatory_settings()
        mandatory_settings.append('invoked_class')
        mandatory_settings.append('time.unit.factor')
        mandatory_settings.append('use.GUI')

        self.current_task_name = selected_task
        self.frames[selected_task] = Frame(self.main_content_frame, background='#FFFFFF')
        self.frames[selected_task].pack(anchor="w", pady=5)

        for each_setting in mandatory_settings:
            setting_frame = Frame(self.frames[selected_task], background='#FFFFFF')
            setting_frame.pack(anchor="w", pady=5)
            initial_value: str = input_setting_values.get(each_setting)
            UIComponentFactory.get_instance(self.root).create_component(each_setting, initial_value, setting_frame)

        automated_task.settings = input_setting_values
        self.render_button_frame(self.frames[selected_task])

    def render_button_frame(self, parent_frame: Frame):
        button_frame = tk.Frame(master=parent_frame, bg='#FFFFFF')
        button_frame.pack(expand=True, fill="both")
        perform_button = tk.Button(button_frame, text='Perform', command=self.handle_perform_button,
                                   bg='#2FACE8', fg='#FFFFFF', width=9, height=1, activeforeground='#FB3D52')
        perform_button.pack(side='left')
        self.pause_button = self.render_pause_button(parent_frame=button_frame)
        self.render_reset_button(parent_frame=button_frame)

    def render_main_content_frame_for_first_task(self, tasks_dropdown: Combobox):
        tasks_dropdown.focus_set()
        tasks_dropdown.current(0)
        tasks_dropdown.event_generate("<<ComboboxSelected>>")

    def handle_tasks_dropdown(self, event):
        if self.current_task_name is not None and self.task_manager.get_task_settings(self.current_task_name):
            persist_settings_to_file(self.current_task_name,
                                     self.task_manager.get_task_settings(self.current_task_name))

        selected_task = event.widget.get()
        if selected_task in self.frames:
            self.frames[self.current_task_name].pack_forget()
            self.frames[selected_task].pack()
        else:
            self.render_main_content_frame(selected_task)

    def handle_perform_button(self):
        automated_task = self.task_manager.get_task_instance(self.current_task_name,
                                                             self.task_manager.get_task_settings(
                                                                 self.current_task_name), self.logger_setup_callback)
        if automated_task.is_alive():
            messagebox.showinfo("Have a task currently running",
                                "Please terminate the current task before run a new one")
            return
        automated_task.start()

    def render_pause_button(self, parent_frame: Frame) -> Button:
        pause_button: Button = tk.Button(master=parent_frame, text='Pause', command=self.handle_pause_button,
                                         bg='#FA6A55', fg='#FFFFFF', width=9, height=1, activeforeground='#FA6A55')
        pause_button.pack(side='left')
        return pause_button

    def handle_pause_button(self):
        automated_task = self.task_manager.get_task_instance(self.current_task_name,
                                                             self.task_manager.get_task_settings(
                                                                 self.current_task_name), self.logger_setup_callback)
        if automated_task.is_alive():
            if self.is_task_currently_pause:
                automated_task.resume()
                self.pause_button.config(text="Pause")
                self.is_task_currently_pause = False
            else:
                automated_task.pause()
                self.pause_button.config(text="Resume")
                self.is_task_currently_pause = True

    def render_reset_button(self, parent_frame: Frame) -> Button:
        reset_button: Button = tk.Button(parent_frame, text='Reset', command=self.handle_reset_button,
                                         bg='#00243D', fg='#FFFFFF', font=('Maersk Headline', 11), width=9, height=1,
                                         activeforeground='#00243D')
        reset_button.pack(side='left')
        return reset_button

    def handle_reset_button(self):
        automated_task = self.task_manager.get_task_instance(self.current_task_name,
                                                             self.task_manager.get_task_settings(
                                                                 self.current_task_name), self.logger_setup_callback)
        if automated_task.is_alive():
            automated_task.stop()
            self.task_manager.update_task_settings(self.current_task_name, {})
            self.progress_bar['value'] = 0
            self.progress_bar_label.configure("Text.Horizontal.TProgressbar",
                                              text="{} {}%".format(self.current_task_name, 0))
            for widget in self.frames[self.current_task_name].winfo_children():
                widget.destroy()
            self.render_main_content_frame(self.current_task_name)
