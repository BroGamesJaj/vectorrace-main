from Model.System.Logging.LogChannelDecoratorBase import LogChannelDecoratorBase


class LevelDecorator(LogChannelDecoratorBase):
    def _decorate_message(self, message: str, level: int) -> str:
        return "[{0}] {1}".format(level, message)
