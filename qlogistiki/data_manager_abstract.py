from abc import ABC, abstractmethod


class AbstractDataManager(ABC):
    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def make_permanent(self):
        pass
