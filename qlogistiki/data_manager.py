from abc import ABC, abstractmethod


class DataManager(ABC):
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


class Test(DataManager):

    def create(self):
        pass


if __name__ == '__main__':
    a = Test()
