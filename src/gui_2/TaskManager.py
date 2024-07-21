from typing import Callable

from src.task.TaskFactory import create_task_instance


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def get_task_instance(self, task_name: str, settings: dict[str, str], callback_before_run_task: Callable):
        if task_name not in self.tasks:
            self.tasks[task_name] = create_task_instance(task_name, settings, callback_before_run_task)
        return self.tasks[task_name]

    def get_task_settings(self, task_name):
        if task_name in self.tasks:
            return self.tasks[task_name].settings
        return {}

    def update_task_settings(self, task_name, settings):
        if task_name in self.tasks:
            self.tasks[task_name].settings = settings
