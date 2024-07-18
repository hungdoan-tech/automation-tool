import tkinter as tk

from src.gui_2.layout.RenderableComponent import RenderableComponent


class Header(RenderableComponent):

    def __init__(self, branding_image_path: str, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.branding_image: str = branding_image_path

    def render(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        self.branding_image_object: tk.PhotoImage = tk.PhotoImage(master=self, file=self.branding_image)
        logo_label: tk.Label = tk.Label(master=self, image=self.branding_image_object, compound=tk.CENTER)
        logo_label.grid_configure(row=0, column=0)
