from src.gui.TextBoxLoggingHandler import setup_textbox_logger


class LoggingHandler:
    def __init__(self, logging_textbox):
        self.logging_textbox = logging_textbox
        self.setup_logger()

    def setup_logger(self):
        setup_textbox_logger(self.logging_textbox)
