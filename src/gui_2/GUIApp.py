import os
import tkinter as tk

from src.gui_2.LoggingHandler import LoggingHandler
from src.gui_2.TaskManager import TaskManager
from src.gui_2.layout.Layout import Layout
from src.gui_2.layout.body.Body import Body
from src.gui_2.layout.footer.Footer import Footer
from src.gui_2.layout.header.Header import Header
from src.gui_2.layout.left_side_bar.LeftSideBar import LeftSideBar
from src.gui_2.layout.right_side_bar.RightSideBar import RightSideBar
from src.setup.packaging.path.PathResolvingService import PathResolvingService


class GUIApp:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.task_manager = TaskManager()
        self.logging_textbox = None
        self.logger_setup_callback = lambda: LoggingHandler(self.logging_textbox).setup_logger()
        self.layout = self.init_layout()

    def init_layout(self) -> Layout:
        self.window.title("Automation Tool")
        self.window.geometry('1920x1080')
        self.window.configure(bg='#FFFFFF')

        layout = Layout(master=self.window, bg='white')
        layout.grid_configure(row=0, column=0, sticky="nsew")

        resource_dir = PathResolvingService.get_instance().resolve('resource')
        branding_image_path = os.path.join(resource_dir, "img", "logo.png")
        header_frame = Header(branding_image_path=branding_image_path, master=layout, bg='red')

        footer_frame = Footer(master=layout, bg='yellow')
        left_frame = LeftSideBar(master=layout, bg='green')
        right_frame = RightSideBar(master=layout, bg='black')
        body_frame = Body(master=layout, bg='blue')

        layout.set_layout(header_frame, left_frame, body_frame, right_frame, footer_frame)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        return layout

    def start(self):
        self.window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    app.start()
