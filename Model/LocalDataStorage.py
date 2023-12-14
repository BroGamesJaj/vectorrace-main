class LocalDataStorage:
    def __init__(self):
        self.__storage = {}

    def get(self, key: str, default_value: any):
        return self.__storage.get(key, default_value)

    def set(self, key, new_value):
        self.__storage[key] = new_value
