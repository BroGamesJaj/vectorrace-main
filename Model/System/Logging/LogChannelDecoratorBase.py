from Model.System.Logging.LogChannelBase import LogChannelBase


class LogChannelDecoratorBase(LogChannelBase):
    def __init__(self, channel_to_decorate: LogChannelBase):
        super().__init__()
        self._channel_to_decorate = channel_to_decorate

    def write(self, message: str, level: int):
        self._channel_to_decorate.write(
            self._decorate_message(message, level),
            level
        )

    def _decorate_message(self, message: str, level: int) -> str:
        raise NotImplementedError()
