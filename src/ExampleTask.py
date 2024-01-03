from logging import Logger

from src.AutomatedTask import AutomatedTask
from src.ThreadLocalLogger import get_current_logger


class ExampleTask(AutomatedTask):
    def mandatory_settings(self) -> set[str]:
        mandatory_keys: set[str] = {'username', 'password', 'excel.path', 'excel.sheet',
                                    'excel.read_column.start_cell', 'hung.path'}
        return mandatory_keys

    def automate(self):
        logger: Logger = get_current_logger()
        logger.info("Has done with some stuff")