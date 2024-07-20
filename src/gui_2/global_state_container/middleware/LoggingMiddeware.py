from logging import Logger

from src.common.ThreadLocalLogger import get_current_logger


def logging_middleware(store, next_dispatch):
    def dispatch(action):
        logger: Logger = get_current_logger()
        logger.info(f"Dispatching action: {action}")

        prev_state = store.get_state()
        logger.info(f"Previous state: {prev_state}")

        result = next_dispatch(action)

        next_state = store.get_state()
        logger.info(f"Next state: {next_state}")

        return result

    return dispatch
