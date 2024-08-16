from os.path import isdir, isfile
from datetime import datetime
from uuid import uuid4

from config import SUPPORT_FORMATS, DEFAULT_SAVE_DIR
from exceptions import UnSupportFileFormatException
from .file_message_type_enum import FileMessageTypeEnum


def write_save_path(message: str, file_accept: bool = False):
    message_type = FileMessageTypeEnum.define_format_type_message(message)

    if message_type == FileMessageTypeEnum.FILE and not file_accept:
        raise FileExistsError(message)

    complete_path: str = ""
    file_type: str = ""

    if message_type == FileMessageTypeEnum.DEFAULT:
        complete_path, file_type = create_complete_filepath()

    if (
        message_type
        in (
            FileMessageTypeEnum.ABSOLUTE,
            FileMessageTypeEnum.FILETYPE_WITH_FILE_NAME,
        )
        and "." in message
    ):
        complete_path, file_type = message.split(".")
        file_type = "." + file_type

    if message_type == FileMessageTypeEnum.FILETYPE_WITH_FILE_NAME:
        complete_path, file_type = create_complete_filepath(complete_path, file_type)

    if message_type == FileMessageTypeEnum.FILETYPE:
        complete_path, file_type = create_complete_filepath(file_format=message)

    if file_type not in SUPPORT_FORMATS:
        raise UnSupportFileFormatException(file_type)

    directory = complete_path.rsplit("/", 1)[0] + "/"
    if not isdir(directory):
        raise NotADirectoryError(complete_path)

    if message_type == FileMessageTypeEnum.UNDEFINED:
        raise ValueError("unexpected message type")

    return complete_path, file_type


def create_complete_filepath(
    file_name: str = None, file_format: str = ".csv"
) -> tuple[str, str]:
    string_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    if not file_name:
        file_name = f"{string_time}_{uuid4()}"

    full_path = DEFAULT_SAVE_DIR + f"{file_name}{file_format}"
    return full_path, file_format

def write_read_path(message: str):
    if not isfile(message):
        raise FileNotFoundError(message)
    complete_path, file_type = message.rsplit(".", 1)
    return complete_path, "." + file_type
