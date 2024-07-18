import os
import tkinter as tk

from src.gui_2.LoggingHandler import LoggingHandler
from src.gui_2.TaskManager import TaskManager
from src.gui_2.layout.Body import Body
from src.gui_2.layout.Footer import Footer
from src.gui_2.layout.Header import Header
from src.gui_2.layout.Layout import Layout
from src.gui_2.layout.LeftSideBar import LeftSideBar
from src.gui_2.layout.RightSideBar import RightSideBar
from src.setup.packaging.path.PathResolvingService import PathResolvingService


class GUIApp:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.task_manager = TaskManager()
        self.logging_textbox = None
        self.logger_setup_callback = lambda: LoggingHandler(self.logging_textbox).setup_logger()

        self.layout = self.init_layout()

        # self.progress_bar_manager = ProgressBarManager(self.layout.progress_bar, self.layout.progress_bar_label)
        # self.event_handler = GUIEventHandler(self.progress_bar_manager)

    def init_layout(self) -> Layout:
        window = tk.Tk()
        window.title("Automation Tool")
        window.geometry('1920x1080')
        window.configure(bg='#FFFFFF')

        layout = Layout(master=window, bg='white')
        layout.grid_configure(row=0, column=0, sticky="nsew")

        resource_dir = PathResolvingService.get_instance().resolve('resource')
        branding_image_path = os.path.join(resource_dir, "img", "logo.png")
        header_frame = Header(branding_image_path=branding_image_path, master=layout, bg='red')

        footer_frame = Footer(master=layout, bg='yellow')
        left_frame = LeftSideBar(master=layout, bg='green')
        right_frame = RightSideBar(master=layout, bg='black')
        body_frame = Body(master=layout, bg='blue')

        layout.set_layout(header_frame, left_frame, body_frame, right_frame, footer_frame)
        layout.render()

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

    def start(self):
        # self.main_content_frame = Frame(master=master_frame, width=1080, height=600, bd=1, relief=tk.SOLID,
        #                                 bg='#FFFFFF', borderwidth=0)
        # self.main_content_frame.pack(padx=10, pady=10)
        #
        # self.render_main_content_frame_for_first_task(tasks_dropdown=tasks_dropdown)
        #
        # self.progress_bar, self.progress_bar_label = self.render_progress_bar(parent_frame=whole_app_frame)
        #
        # self.logging_textbox = self.render_textbox_logger(parent_frame=whole_app_frame)

        self.window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    app.start()
