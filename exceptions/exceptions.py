class UnSupportFileFormatException(Exception):
    def __init__(self, file_type):
        self.message = f"{file_type} is unsupported file format"
        super().__init__(self.message)
