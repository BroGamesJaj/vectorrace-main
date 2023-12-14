from Model.System.SettingsBase import SettingsBase


class Settings(SettingsBase):
    def _set_commands(self):
        self._add_command("TracksFolder", "TF")
        self._add_command("TrackIndex", "TI")
        self._add_command("TrackName", "TN")
        self._add_command("DriversFolder", "DF")
        self._add_command("LogsFolder", "LF")
        self._add_command("LogIndex", "LI")
        self._add_command("LogName", "LN")
        self._add_command("LogType", "LT")
        self._add_command("VisualizationType", "VT")
