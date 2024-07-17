from src.gui_2.GUIEventHandler import GUIEventHandler
from src.gui_2.layout.Layout import LayoutController
from src.gui_2.LoggingHandler import LoggingHandler
from src.gui_2.ProgressBarManager import ProgressBarManager
from src.gui_2.TaskManager import TaskManager
import tkinter as tk


class GUIApp:
    def __init__(self, root):
        self.root = root
        self.task_manager = TaskManager()
        self.logging_textbox = None
        self.logger_setup_callback = lambda: LoggingHandler(self.logging_textbox).setup_logger()

        self.ui_manager = LayoutController(root, self.task_manager, self.logger_setup_callback)
        self.ui_manager.setup_ui()

        self.progress_bar_manager = ProgressBarManager(self.ui_manager.progress_bar, self.ui_manager.progress_bar_label)
        self.event_handler = GUIEventHandler(self.progress_bar_manager)

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    app.start()
