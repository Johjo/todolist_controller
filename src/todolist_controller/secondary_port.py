from abc import ABC, abstractmethod
from uuid import UUID

from todolist_controller.primary_port import TaskPresentation


class TodolistUseCasePort(ABC):
    @abstractmethod
    def open_task(self, todolist_id: UUID, task_id: UUID, task_description: str) -> None:
        pass

    @abstractmethod
    def tasks(self, todolist_id: UUID) -> list[TaskPresentation]:
        pass


class UuidGeneratorPort(ABC):
    @abstractmethod
    def generate_uuid(self) -> UUID:
        pass
