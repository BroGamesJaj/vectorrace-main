from Model.System.Logging.LogChannelBase import LogChannelBase


class FileLogChannel(LogChannelBase):
    def __init__(self, file_name, line_feed="\n", log_level: int = -1):
        super().__init__(log_level)
        self._file_name = file_name
        self._line_feed = line_feed

    def _process_message(self, message):
        with open(self._file_name, "a") as file:
            file.write(message)
            file.write(self._line_feed)
