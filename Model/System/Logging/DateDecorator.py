from datetime import datetime

from Model.System.Logging.LogChannelDecoratorBase import LogChannelDecoratorBase


class DateDecorator(LogChannelDecoratorBase):
    def _decorate_message(self, message: str, level: int) -> str:
        return "{0} {1}".format(datetime.now().strftime("%Y.%m.%d"), message)
