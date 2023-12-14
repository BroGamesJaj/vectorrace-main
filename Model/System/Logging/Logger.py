from Model.System.Logging.LogChannelBase import LogChannelBase


class Logger:
    # 1-Critical, 2-Error, 3-Warning, 4-Info, 5-Verbose
    def __init__(self, log_level=3):
        self._log_level = log_level
        self._channels = []

    def set_level(self, new_log_level):
        self._log_level = new_log_level

    def add_channel(self, new_channel: LogChannelBase):
        self._channels.append(new_channel)

    def log(self, message: str, level: int):
        if level <= self._log_level:
            for c in self._channels:
                c.write(message, level)
