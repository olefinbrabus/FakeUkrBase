class UnSupportFileFormatException(Exception):
    def __init__(self, file_type):
        self.message = f"{file_type} is unsupported file format"
        super().__init__(self.message)


class ConflictDataTakenException(Exception):
    def __init__(self, message1, message2):
        self.message = f"{message1} has conflict with {message2}"
        super().__init__(self.message)
