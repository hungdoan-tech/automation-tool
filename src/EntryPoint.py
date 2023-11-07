import os
import threading
import importlib
from types import ModuleType
from typing import List

from AutomatedTask import AutomatedTask
from Utilities import load_settings_from_file, escape_bat_file_special_chars
from Constants import ROOT_DIR
from Logger import centralized_logger


def escape_special_chars_to_embedded_python_to_bat():
    escape_bat_file_special_chars(input_file=os.path.join(ROOT_DIR, 'input', 'MinifiedDownloadSource.input'))


if __name__ == '__main__':
    # escape_special_chars_to_embedded_python_to_bat()

    setting_file = os.path.join(ROOT_DIR, 'input', 'InvokedClasses.input')
    settings: dict[str, str] = load_settings_from_file(setting_file)
    if settings['invoked_classes'] is None:
        centralized_logger.error('You have not provided the needed to invoke classes/tasks')
        raise Exception('You have not provided the needed to invoke classes/tasks')
    defined_classes: set[str] = set(settings['invoked_classes'].split(','))

    for invoked_class in defined_classes:
        invoked_class = invoked_class.strip()
        clazz_module: ModuleType = importlib.import_module(invoked_class)
        clazz = getattr(clazz_module, invoked_class)

        setting_file = os.path.join(ROOT_DIR, 'input', '{}.input'.format(invoked_class))
        settings: dict[str, str] = load_settings_from_file(setting_file)

        centralized_logger.info("-------------------------------------------------------------------------------------------------------------")
        automated_task: AutomatedTask = clazz(settings)
        automated_task.automate()

        running_task_thread = threading.Thread(target=automated_task.automate,
                                               daemon=True)
        running_task_thread.start()
