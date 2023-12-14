from Model.System.Logging.LogChannelBase import LogChannelBase


class ConsoleLogChannel(LogChannelBase):
    def _process_message(self, message):
        print(message)
