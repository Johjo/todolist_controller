from abc import ABC, abstractmethod
from uuid import UUID


class TodolistUseCasePort(ABC):
    @abstractmethod
    def open_task(self, todolist_id: UUID, task_id: UUID, task_description: str) -> None:
        pass



class UuidGeneratorPort(ABC):
    @abstractmethod
    def generate_uuid(self) -> UUID:
        pass
