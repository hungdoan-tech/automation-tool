import time
from logging import Logger

from src.task.AutomatedTask import AutomatedTask
from src.common.ThreadLocalLogger import get_current_logger


class ExampleTask(AutomatedTask):

    def __init__(self, settings: dict[str, str]):
        super().__init__(settings)

    def mandatory_settings(self) -> list[str]:
        mandatory_keys: list[str] = ['username', 'password', 'excel.path', 'excel.sheet',
                                     'excel.read_column.start_cell', 'hung.path']
        return mandatory_keys

    def automate(self):
        logger: Logger = get_current_logger()

        self.current_element_count = 0
        self.total_element_size = 10

        while self.current_element_count < self.total_element_size:
            self.current_element_count = self.current_element_count + 1
            logger.info("Example automated task - running at item {}".format(self.current_element_count))
            time.sleep(2)
