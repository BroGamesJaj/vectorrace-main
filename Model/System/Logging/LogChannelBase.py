class LogChannelBase:
    def __init__(self, log_level: int = -1):
        self._log_level = log_level

    # 1-Critical, 2-Error, 3-Warning, 4-Info, 5-Verbose
    def set_level(self, new_log_level):
        self._log_level = new_log_level

    def write(self, message: str, level: int):
        if self._log_level < 0 or level <= self._log_level:
            self._process_message(message)

    def _process_message(self, message):
        raise NotImplementedError()
