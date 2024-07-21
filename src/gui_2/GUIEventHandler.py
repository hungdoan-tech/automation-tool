from logging import Logger

from src.common.logging.ThreadLocalLogger import get_current_logger
from src.observer.Event import Event
from src.observer.EventHandler import EventHandler
from src.observer.PercentChangedEvent import PercentChangedEvent


class GUIEventHandler(EventHandler):
    def __init__(self, progress_bar_manager):
        self.progress_bar_manager = progress_bar_manager

    def handle_incoming_event(self, event: Event) -> None:
        logger: Logger = get_current_logger()

        if isinstance(event, PercentChangedEvent):

            if self.automated_task is None:
                logger.error(f'The PercentChangedEvent for ${event.task_name} but no task in action in GUI app')
                return

            current_task_name = type(self.automated_task).__name__
            if event.task_name is not current_task_name:
                logger.warning(f'The PercentChangedEvent for ${event.task_name} is '
                               f'not match with the current task ${current_task_name}')
                return

            distance_between_ui_percent_n_event_percent: float = (
                    event.current_percent - float(self.progress_bar['value']))
            default_distance_of_task: float = self.automated_task.get_percentage_distance()
            if distance_between_ui_percent_n_event_percent > default_distance_of_task:
                return

            self.progress_bar['value'] = round(event.current_percent)
            self.progress_bar_label.configure("Text.Horizontal.TProgressbar",
                                              text="{} {}%".format(current_task_name,
                                                                   event.current_percent))
