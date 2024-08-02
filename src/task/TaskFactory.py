import importlib
import os
from types import ModuleType
from typing import Callable

from src.common.util.FileUtil import find_module, load_key_value_from_file_properties
from src.setup.packaging.path.PathResolvingService import PathResolvingService
from src.task.AutomatedTask import AutomatedTask

cache: dict[str, ModuleType] = {}


def create_task_instance(task_name: str, setting_states: dict[str, str],
                         callback_before_run_task: Callable[[], None]) -> AutomatedTask:
    if cache.get(task_name):
        clazz = getattr(cache.get(task_name), task_name)
        automated_task: AutomatedTask = clazz(setting_states, callback_before_run_task)
        return automated_task

    module_path = find_module(PathResolvingService.get_instance().get_task_dir(), task_name)
    if module_path is None:
        raise FileNotFoundError(f"Task file {task_name}.py not found in {module_path} and its subdirectories.")

    clazz_module: ModuleType = importlib.import_module(module_path)
    cache[task_name] = clazz_module
    clazz = getattr(clazz_module, task_name)
    automated_task: AutomatedTask = clazz(setting_states, callback_before_run_task)
    return automated_task


def get_task_settings(active_task: str) -> dict[str, str]:
    setting_file = os.path.join(PathResolvingService.get_instance().get_input_dir(),
                                '{}.properties'.format(active_task))
    if not os.path.exists(setting_file):
        with open(setting_file, 'w'):
            pass

    settings: dict[str, str] = load_key_value_from_file_properties(setting_file)
    settings['invoked_class'] = active_task

    if settings.get('time.unit.factor') is None:
        settings['time.unit.factor'] = '1'

    if settings.get('use.GUI') is None:
        settings['use.GUI'] = 'True'

    return settings
