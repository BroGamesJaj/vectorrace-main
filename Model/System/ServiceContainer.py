class ServiceContainer:
    def __init__(self):
        self.__services = []

    def append(self, new_service):
        self.__services.append(new_service)

    def update(self, new_service):
        updated = False
        for i in range(len(self.__services)):
            if isinstance(self.__services[i], type(new_service)):
                self.__services[i] = new_service
                updated = True

        if not updated:
            self.append(new_service)

    def get_first(self, service_type):
        for s in self.__services:
            if isinstance(s, service_type):
                return s
