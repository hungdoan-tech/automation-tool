import os
import threading
import importlib
import uuid
from logging import Logger
from threading import Thread
from types import ModuleType

from Utilities import load_settings_from_file, escape_bat_file_special_chars
from Constants import ROOT_DIR
from AutomatedTask import AutomatedTask
from ThreadLocalLogger import create_thread_local_logger


def escape_special_chars_to_embedded_python_to_bat():
    escape_bat_file_special_chars(input_file=os.path.join(ROOT_DIR, 'input', 'MinifiedDownloadSource.input'))


if __name__ == '__main__':
    # escape_special_chars_to_embedded_python_to_bat()

    setting_file: str = os.path.join(ROOT_DIR, 'input', 'InvokedClasses.input')
    settings: dict[str, str] = load_settings_from_file(setting_file)
    if settings['invoked_classes'] is None:
        raise Exception('You have not provided the needed to invoke classes/tasks')
    defined_classes: list[str] = [class_name.strip() for class_name in settings['invoked_classes'].split(',')]

    running_threads: list[Thread] = []
    for invoked_class in defined_classes:
        logger: Logger = create_thread_local_logger(class_name=invoked_class, thread_uuid=str(uuid.uuid4()))

        logger.info('Invoking class {}'.format(invoked_class))
        clazz_module: ModuleType = importlib.import_module(invoked_class)
        clazz = getattr(clazz_module, invoked_class)

        setting_file = os.path.join(ROOT_DIR, 'input', '{}.input'.format(invoked_class))
        settings: dict[str, str] = load_settings_from_file(setting_file)

        automated_task: AutomatedTask = clazz(settings)
        running_task_thread: Thread = threading.Thread(target=automated_task.automate,
                                                       daemon=False)
        running_task_thread.start()
        running_threads.append(automated_task)

    for thread in running_threads:
        thread.join(timeout=5 * 60)
