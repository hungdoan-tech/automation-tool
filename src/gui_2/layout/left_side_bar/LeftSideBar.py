import os
from tkinter import ttk
from tkinter.ttk import Scrollbar

from src.gui_2.global_state.Store import store
from src.gui_2.global_state.action.TaskAction import TaskAction
from src.gui_2.layout.Component import Component
from src.setup.packaging.path.PathResolvingService import PathResolvingService


class LeftSideBar(Component):
    def render(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        # self.grid_columnconfigure(index=1, weight=1)

        tree_scroll: Scrollbar = ttk.Scrollbar(master=self)
        tree_scroll.grid(row=0, column=1, sticky='ns')

        treeview = ttk.Treeview(master=self, selectmode="extended", yscrollcommand=tree_scroll.set,
                                columns=())  # No additional columns
        treeview.grid(row=0, column=0, sticky='nsew')
        tree_scroll.config(command=treeview.yview)

        treeview.column('#0', width=0)  # Adjust width as needed
        treeview.heading('#0', text="Task type")

        path_to_tasks_module: str = PathResolvingService.get_instance().resolve("src", "task")
        treeview_data, parent_set = self.__populate_treeview_data(path_to_tasks_module)
        self.parent_set = parent_set

        for item in treeview_data:
            treeview.insert(parent=item[0], index="end", iid=item[2], text=item[3])

            if item[0] in self.parent_set:
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
        store.dispatch(TaskAction.CHANGE_ACTIVE_TASK.invoke(selected_task))

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
