import time
from logging import Logger
from typing import Callable

from src.task.AutomatedTask import AutomatedTask
from src.common.ThreadLocalLogger import get_current_logger


class ExampleTask(AutomatedTask):

    def __init__(self, settings: dict[str, str], callback_before_run_task: Callable[[], None]):
        super().__init__(settings, callback_before_run_task)

    def mandatory_settings(self) -> list[str]:
        mandatory_keys: list[str] = ['username', 'password', 'excel.path', 'excel.sheet',
                                     'excel.read_column.start_cell', 'hung.path']
        return mandatory_keys

    def automate(self):
        logger: Logger = get_current_logger()

        self.current_element_count = 0
        self.total_element_size = 10

        while self.current_element_count < self.total_element_size:

            if self.terminated is True:
                return

            with self.pause_condition:

                while self.paused:
                    self.pause_condition.wait()

                if self.terminated is True:
                    return

            self.current_element_count = self.current_element_count + 1
            logger.info("Example automated task - running at item {}".format(self.current_element_count))
            time.sleep(2)
