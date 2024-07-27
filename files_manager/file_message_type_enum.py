from os.path import isfile, isabs
from enum import Enum

from config import DEFAULT_SAVE_DIR


class FileMessageTypeEnum(Enum):
    UNDEFINED = 0
    DEFAULT = 1
    ABSOLUTE = 2
    FILETYPE = 3
    FILETYPE_WITH_FILE_NAME = 4
    FILE = 5

    @staticmethod
    def define_format_type_message(
        undefined_message_format: str,
    ) -> "FileMessageTypeEnum":
        if isabs(undefined_message_format.rsplit("/", 1)[0]):
            return FileMessageTypeEnum.ABSOLUTE

        if isfile(undefined_message_format):
            return FileMessageTypeEnum.FILE

        if not message_contains_slash(undefined_message_format):
            if undefined_message_format.startswith("."):
                return FileMessageTypeEnum.FILETYPE
            if "." in undefined_message_format:
                return FileMessageTypeEnum.FILETYPE_WITH_FILE_NAME

        if undefined_message_format == "default":
            return FileMessageTypeEnum.DEFAULT

        return FileMessageTypeEnum.UNDEFINED


def message_contains_slash(undefined_format: str) -> bool:
    return "/" in undefined_format
