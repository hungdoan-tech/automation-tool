import tkinter as tk
from tkinter import ttk


class CloseableNotebook(ttk.Notebook):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.bind("<Button-1>", self.on_click)

    def add_tab(self, frame, text):
        tab_id = self.add(frame, text=text)
        close_button = tk.Button(self, text="X", command=lambda: self.close_tab(tab_id))
        # Store close button reference
        self.tab(tab_id=tab_id, text=f"{text} ")
        self._add_close_button(tab_id, close_button)

    def _add_close_button(self, tab_id, button):
        # Ensure button is placed in the tab's header
        tab_frame = self.nametowidget(tab_id)
        button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    def close_tab(self, tab_id):
        self.forget(tab_id=tab_id)

    def on_click(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget.cget("text") == "X":
            tab_id = self.index("current")
            self.close_tab(tab_id)


# Create the main window
root = tk.Tk()
root.geometry("400x300")

# Create the CloseableNotebook
notebook = CloseableNotebook(root)
notebook.pack(fill="both", expand=True)

# Add tabs with close buttons
frame1 = tk.Frame(notebook, bg="lightblue")
notebook.add_tab(frame1, "Tab 1")

frame2 = tk.Frame(notebook, bg="lightgreen")
notebook.add_tab(frame2, "Tab 2")

root.mainloop()
