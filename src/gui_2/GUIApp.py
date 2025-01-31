import os
import tkinter as tk
from tkinter import ttk, Frame

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
        self.layout = self.init_layout()

    def init_layout(self) -> Layout:
        self.window.title("MEK AC - Automation Tool")

        window_width = 1600
        window_height = 900
        self.window.geometry(f'{window_width}x{window_height}')

        self.window.update()

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.window.geometry(f'{window_width}x{window_height}+{x_cordinate}+{y_cordinate}')
        self.window.minsize(1600, 900)

        self.window.configure()

        layout = Layout(master=self.window, bg='white')
        layout.grid_configure(row=0, column=0, sticky="nsew")

        resource_dir = PathResolvingService.get_instance().resolve('resource')
        branding_image_path = os.path.join(resource_dir, "img", "logo.png")
        header_frame = Header(branding_image_path=branding_image_path, master=layout, bg='#F7F7F7')

        footer_frame = Footer(master=layout)
        left_frame = LeftSideBar(master=layout, bg='#42B0D5')
        right_frame = RightSideBar(master=layout, bg='#42B0D5')
        body_frame = Body(master=layout)

        layout.set_layout(header_frame, left_frame, body_frame, right_frame, footer_frame)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        return layout

    def start(self):
        self.window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.option_add("*tearOff", False)

    theme_path: str = os.path.join(PathResolvingService.get_instance().resolve("resource"),
                                   "theme", "forest-light.tcl")
    root.tk.call("source", theme_path)

    style = ttk.Style(root)
    style.theme_use("forest-light")

    app.start()
