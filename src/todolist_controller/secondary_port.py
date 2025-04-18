from abc import ABC, abstractmethod
from uuid import UUID



class UuidGeneratorPort(ABC):
    @abstractmethod
    def generate_uuid(self) -> UUID:
        pass
