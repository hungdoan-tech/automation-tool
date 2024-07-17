from tkinter import Frame
import tkinter as tk

from src.gui_2.layout.Renderable import Renderable


class Body(Renderable):

    def __init__(self, master_frame: Frame):
        self.main_content_frame = Frame(master=master_frame, width=1080, height=600, bd=1, relief=tk.SOLID,
                                        bg='#FFFFFF', borderwidth=0)
        self.main_content_frame.pack(padx=10, pady=10)

        self.render_main_content_frame_for_first_task(tasks_dropdown=tasks_dropdown)

        self.progress_bar, self.progress_bar_label = self.render_progress_bar(parent_frame=whole_app_frame)

        self.logging_textbox = self.render_textbox_logger(parent_frame=whole_app_frame)

    def render(self):
        pass