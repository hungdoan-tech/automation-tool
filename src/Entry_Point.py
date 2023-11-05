import os

from Automated_Ticket_CottonOn import AutomatedTicketCottonOn
from Automated_Task import AutomatedTask
from Utilities import load_settings_from_file, escape_bat_file_special_chars
from Constants import ROOT_DIR
from src.Logger import centralized_logger


def escape_special_chars_to_embedded_python_to_bat():
    escape_bat_file_special_chars(input_file=os.path.join(ROOT_DIR, 'input', 'minified_download_source.py'))


if __name__ == '__main__':
    # escape_special_chars_to_embedded_python_to_bat()
    centralized_logger.info("-------------------------------------------------------------------------------------------------------------")
    setting_file = os.path.join(ROOT_DIR, 'input', 'settings.input')
    if not os.path.exists(setting_file):
        raise Exception("The settings file is not existed. Please providing it !")
    settings: dict[str, str] = load_settings_from_file(setting_file)

    automatedTask: AutomatedTask = AutomatedTicketCottonOn(settings)
    automatedTask.automate()
