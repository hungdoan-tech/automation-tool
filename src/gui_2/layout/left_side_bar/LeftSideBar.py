from tkinter import ttk
from tkinter.ttk import Scrollbar

from src.gui_2.layout.Component import Component


class LeftSideBar(Component):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

    def render(self):
        # Scrollbar
        tree_scroll: Scrollbar = ttk.Scrollbar(master=self)
        tree_scroll.pack(side="right", fill="y")

        # Treeview
        treeview = ttk.Treeview(master=self, selectmode="extended", yscrollcommand=tree_scroll.set, columns=(1, 2),
                                height=12)
        treeview.pack(expand=True, fill="both")
        tree_scroll.config(command=treeview.yview)

        # Treeview columns
        treeview.column("#0", width=120)
        treeview.column(1, anchor="w", width=120)
        treeview.column(2, anchor="w", width=120)

        # Treeview headings
        treeview.heading("#0", text="Column 1", anchor="center")
        treeview.heading(1, text="Column 2", anchor="center")
        treeview.heading(2, text="Column 3", anchor="center")

        # Define treeview data
        treeview_data = []

        # Insert treeview data
        for item in treeview_data:
            treeview.insert(parent=item[0], index="end", iid=item[2], text=item[3], values=item[4])
            if item[0] == "" or item[2] in (8, 12):
                treeview.item(item[2], open=True)  # Open parents

        # Select and scroll
        treeview.selection_set(10)
        treeview.see(7)
