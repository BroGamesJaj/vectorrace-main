class SettingsBase:
    def __init__(self, args: list, command_prefix=None, parameter_delimiter=":"):
        self._prefix = command_prefix
        self._delimiter = parameter_delimiter
        self._args = args
        self._commands = []
        self._short_commands = []
        self._set_commands()
        self._parameters = {}
        self._parse()

    def _add_command(self, command: str, short: str):
        self._commands.append(command.lower())
        self._short_commands.append(short.lower())

    def _set_commands(self):
        raise NotImplementedError()

    def _parse(self):
        for i in range(1, len(self._args)):
            if self._prefix is None or self._args[i].startswith(self._prefix):
                parts = [p.strip() for p in self._args[i].split(self._delimiter)]
                if len(parts) == 2:
                    command = parts[0].lower()
                    for ci in range(len(self._short_commands)):
                        if command == self._short_commands[ci]:
                            self._parameters[self._commands[ci]] = parts[1]

                    for c in self._commands:
                        if command == c:
                            self._parameters[c] = parts[1]

    def get_args(self):
        return self._args.copy()

    def get_parameter_by_key(self, key: str, default_value=None):
        return self._parameters.get(key.lower(), default_value)

    def get_parameter_by_index(self, index: int):
        return self._args[index]
