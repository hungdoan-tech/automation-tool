import os.path
import re
import copy
import openpyxl
import zipfile
import time

from openpyxl.cell.cell import Cell
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from Logger import centralized_logger
from Constants import ROOT_DIR


def get_excel_data_in_column_start_at_row(file_path, sheet_name, start_cell) -> set[str]:
    column: str = 'A'
    start_row: int = 0

    result = re.search('([a-zA-Z]+)(\d+)', start_cell)
    if result:
        column = result.group(1)
        start_row = int(result.group(2))

    centralized_logger.info(
        r"Read data from file {} at sheet {}, collect all data at column {} start from row {}".format(
            file_path, sheet_name, column, start_row))
    workbook: Workbook = openpyxl.load_workbook(filename=r'{}'.format(file_path), data_only=True, keep_vba=True)
    worksheet: Worksheet = workbook[sheet_name]

    values: set[str] = set()
    runner: int = 0
    max_index = start_row - 1
    for cell in worksheet[column]:
        cell: Cell = cell

        if runner < max_index:
            runner += 1
            continue

        if cell.value is None:
            continue

        values.add(str(cell.value))
        runner += 1

    if len(values) == 0:
        centralized_logger.error(
            r'Not containing any data from file {} at sheet {} at column {} start from row {}'.format(
                file_path, sheet_name, column, start_row))
        raise Exception("Not containing required data in the specified place in file Excel")

    centralized_logger.info('Collect data from excel file successfully')
    return values


def load_settings_from_file(setting_file: str) -> dict[str, str]:
    if not os.path.exists(setting_file):
        raise Exception("The settings file {} is not existed. Please providing it !".format(setting_file))

    settings: dict[str, str] = {}
    centralized_logger.info('Start loading settings from file')
    with open(setting_file, 'r') as setting_file_stream:
        for line in setting_file_stream:

            line = line.replace("\n", "").strip()
            if len(line) == 0 or line.startswith("#"):
                continue

            key_value: list[str] = line.split("=")
            key: str = key_value[0].strip()
            value: str = key_value[1].strip()
            settings[key] = value

    return settings


def validate_keys_of_settings(settings: dict[str, str],
                              mandatory_settings: set[str]) -> list[str]:
    error_messages: list[str] = []
    for key in mandatory_settings:

        value = settings[str(key)]
        if value is None:
            error_messages.append('{} is missing'.format(key))

        if len(value) == 0:
            error_messages.append('{} is missing'.format(key))

    return error_messages


def decode_url(url: str) -> str:
    decoded: str = ""
    index: int = 0

    while index < len(url):
        if url[index] == '%':
            hex_char = url[index + 1: index + 3]  # Extract the hexadecimal representation of the character
            decoded += chr(int(hex_char, 16))  # Convert it to an integer and then to a character
            index += 3  # Skip the '%' and two hexadecimal digits
        else:
            decoded += url[index]
            index += 1

    return decoded


def extract_zip(zip_file_path: str,
                extracted_dir: str,
                sleep_time_before_extract: int = 1,
                delete_all_others: bool = False) -> None:
    time.sleep(sleep_time_before_extract)
    if not os.path.isfile(zip_file_path) or not zip_file_path.lower().endswith('.zip'):
        raise Exception('{} is not a zip file'.format(zip_file_path))

    zip_file_path = zip_file_path.replace('\\', '/')
    file_name_contain_extension: str = zip_file_path.split('/')[-1]
    clean_file_name: str = file_name_contain_extension.split('.')[0]

    if not extracted_dir.endswith('/') and not extracted_dir.endswith('\\'):
        extracted_dir += '\\'

    if clean_file_name not in extracted_dir:
        extracted_dir = r'{}{}'.format(extracted_dir, clean_file_name)
        if not os.path.exists(extracted_dir):
            os.mkdir(extracted_dir)

    centralized_logger.debug(r'Start extracting file {} into {}'.format(zip_file_path, extracted_dir))

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir)

    os.remove(zip_file_path)
    centralized_logger.debug(r'Extracting file {} to {} successfully'.format(zip_file_path, extracted_dir))

    if delete_all_others:
        current_dir: str = os.path.dirname(os.path.abspath(zip_file_path))
        remove_all_files_in_folder(current_dir, True)


def escape_bat_file_special_chars(input_file: str = '.\\DownloadSource.py',
                                  output_file: str = os.path.join(ROOT_DIR, 'output', 'EscapedCharsEmbeddedPythonToBat.output')) -> None:
    if not os.path.exists(input_file):
        raise Exception('invalid input')

    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w') as outputStream:
        with open(input_file, 'r') as inputStream:
            for line in inputStream:
                outputStream.write('echo ' + escape_for_batch(line))


def escape_for_batch(text) -> str:
    special_chars: set[str] = {'%', '!', '^', '<', '>', '&', '|', '=', '+', ';', ',', '(', ')', '[', ']', '{', '}', '"'}
    new_line: str = ''
    # Escape each special character with a caret (^)
    for char in text:
        if char in special_chars:
            new_line += f'^{char}'
        else:
            new_line += char

    return new_line


def join_set_of_elements(container: set[str], delimiter: str) -> str:
    successful_files: str = ''
    for element in container:
        successful_files += element + delimiter
    return successful_files


def check_parent_folder_contain_all_required_sub_folders(parent_folder: str,
                                                         required_sub_folders: set[str],
                                                         delete_all_others: bool = False) -> (bool, set[str], set[str]):
    contained_set: set[str] = set()
    for dir_name in os.listdir(parent_folder):
        full_dir_name = os.path.join(parent_folder, dir_name)
        if os.path.isdir(full_dir_name) and dir_name in required_sub_folders:
            contained_set.add(dir_name)
            required_sub_folders.discard(dir_name)

    is_all_contained: bool = len(required_sub_folders) == 0
    not_contained_set: set[str] = copy.deepcopy(required_sub_folders)
    return is_all_contained, contained_set, not_contained_set


def remove_all_files_in_folder(folder_path: str, only_files: bool = False) -> None:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            if not only_files:
                remove_all_files_in_folder(file_path)
    centralized_logger.debug(
        r'Deleted all other generated files in {} while running exception the extracted folder'.format(folder_path))
