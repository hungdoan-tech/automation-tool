import os
from tkinter import ttk, Frame
from tkinter.ttk import Scrollbar

from src.gui_2.global_state.Store import store
from src.gui_2.global_state.action.TaskNameAction import set_task_name
from src.gui_2.layout.Component import Component
from src.setup.packaging.path.PathResolvingService import PathResolvingService


class LeftSideBar(Component):
    def render(self):
        # col_num = 5
        # runner = 0
        # while runner < col_num:
        #     self.grid_rowconfigure(index=runner, weight=1)
        #     self.grid_columnconfigure(index=runner, weight=1)
        #     runner += 1
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        inner_frame = Frame(master=self)
        inner_frame.grid_rowconfigure(index=0, weight=1)
        inner_frame.grid_rowconfigure(index=0, weight=1)
        inner_frame.grid_configure(row=0, column=0, rowspan=1, columnspan=1, sticky='nsew')

        tree_scroll: Scrollbar = ttk.Scrollbar(master=inner_frame)
        tree_scroll.grid_configure(row=0, column=4, rowspan=5, columnspan=1, sticky='nse')
        treeview = ttk.Treeview(master=inner_frame, selectmode="extended", yscrollcommand=tree_scroll.set,
                                columns=['0'])
        treeview.grid_configure(row=0, column=1, rowspan=5, columnspan=3, sticky='nsew')
        tree_scroll.config(command=treeview.yview)
        treeview.column('#0')
        treeview.heading('#0', text="Task type")

        path_to_tasks_module: str = PathResolvingService.get_instance().resolve("src", "task")
        treeview_data, parent_set = self.__populate_treeview_data(path_to_tasks_module)
        self.parent_set = parent_set

        for item in treeview_data:
            treeview.insert(parent=item[0], index="end", iid=item[2], text=item[3])

            if parent_set.__contains__(item[0]):
                treeview.item(item[0], open=True)

        treeview.bind("<ButtonRelease-1>", self.on_item_click)
        self.treeview = treeview

    def on_item_click(self, event):
        item_id = self.winfo_containing(event.x_root, event.y_root).focus()
        item_id: int = int(item_id)

        if item_id is None:
            return

        if self.parent_set.__contains__(item_id):
            return

        selected_task = self.treeview.item(item=item_id, option='text')
        store.dispatch(set_task_name(selected_task))

    def __populate_treeview_data(self, directory: str):
        treeview_data = []
        parent_set: set[str | int] = {""}
        excluding_files = {'AutomatedTask.py', 'DesktopTask.py', 'WebTask.py', 'TaskFactory.py', '__init__.py'}

        def traverse_dir(parent_id, path):
            nonlocal treeview_data, parent_set
            entries = os.listdir(path)
            for entry in entries:
                entry_path = os.path.join(path, entry)

                if entry == '__pycache__':
                    continue

                if os.path.isdir(entry_path):
                    entry_id = len(treeview_data) + 1
                    treeview_data.append((parent_id, "end", entry_id, entry, ()))
                    parent_set.add(entry_id)
                    traverse_dir(entry_id, entry_path)
                    continue

                if entry in excluding_files:
                    continue

                entry_id = len(treeview_data) + 1
                treeview_data.append((parent_id, "end", entry_id, os.path.basename(entry)))

        traverse_dir("", directory)
        return treeview_data, parent_set
