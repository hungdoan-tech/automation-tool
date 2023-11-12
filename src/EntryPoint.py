import os
import threading
import importlib
import uuid
from logging import Logger
from threading import Thread
from types import ModuleType

from Utilities import load_settings_from_file, escape_bat_file_special_chars, validate_keys_of_settings
from Constants import ROOT_DIR
from AutomatedTask import AutomatedTask
from ThreadLocalLogger import create_thread_local_logger, get_current_logger


def escape_special_chars_to_embedded_python_to_bat():
    escape_bat_file_special_chars(input_file=os.path.join(ROOT_DIR, 'input', 'MinifiedDownloadSource.input'))


if __name__ == "__main__":
    # escape_special_chars_to_embedded_python_to_bat()

    setting_file: str = os.path.join(ROOT_DIR, 'input', 'InvokedClasses.input')
    settings: dict[str, str] = load_settings_from_file(setting_file)
    validate_keys_of_settings(settings, {'invoked_classes', 'run.sequentially'})
    defined_classes: list[str] = [class_name.strip() for class_name in settings['invoked_classes'].split(',')]
    run_sequentially: bool = 'True'.lower() == str(settings['run.sequentially']).lower()

    running_threads: list[Thread] = []
    for invoked_class in defined_classes:

        logger: Logger = get_current_logger()
        logger.info('Invoking class {}'.format(invoked_class))

        clazz_module: ModuleType = importlib.import_module(invoked_class)
        clazz = getattr(clazz_module, invoked_class)

        setting_file = os.path.join(ROOT_DIR, 'input', '{}.input'.format(invoked_class))
        settings: dict[str, str] = load_settings_from_file(setting_file)
        settings['invoked_class'] = invoked_class

        automated_task: AutomatedTask = clazz(settings)

        if run_sequentially:
            automated_task.perform()
            continue

        # run concurrently
        running_task_thread: Thread = threading.Thread(target=automated_task.perform,
                                                       daemon=False)
        running_task_thread.start()
        running_threads.append(running_task_thread)

    for thread in running_threads:
        thread.join(timeout=60 * 60)
