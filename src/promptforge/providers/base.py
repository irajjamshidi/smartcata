from abc import ABC, abstractmethod
class Provider(ABC):
    name: str
    @abstractmethod
    def compile(self, task): ...
