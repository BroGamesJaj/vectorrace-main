class DriverLog:
    SPLIT_COUNT = 1

    def __init__(self, identifier, next_split_index=1):
        self._identifier = identifier
        self._splits_crossed = 0
        self._last_split_iteration = 0
        self._max_speed = 0
        self._next_split_index = next_split_index

    def get_identifier(self):
        return self._identifier

    def get_next_split_index(self):
        return self._next_split_index

    def get_splits_crossed(self):
        return self._splits_crossed

    def get_last_split_iteration(self):
        return self._last_split_iteration

    def get_max_speed(self):
        return self._max_speed

    def add_split(self, iteration):
        self._last_split_iteration = iteration
        self._splits_crossed += 1
        self._next_split_index += 1
        if self._next_split_index >= DriverLog.SPLIT_COUNT:
            self._next_split_index = 0

    def set_speed(self, new_speed):
        if self._max_speed < new_speed:
            self._max_speed = new_speed

    def __str__(self):
        return "{0} crossed {1} splits in {2} iterations with max speed {3}".format(
            self._identifier,
            self._splits_crossed,
            self._last_split_iteration,
            self._max_speed
        )
