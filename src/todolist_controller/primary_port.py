from abc import abstractmethod
from uuid import UUID

from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation


class TodolistControllerPort:
    @abstractmethod
    def create_todolist(self) -> UUID:
        pass

    @abstractmethod
    def open_task(self, todolist_key: UUID, title: str, description: str) -> UUID:
        pass

    @abstractmethod
    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation:
        pass

    @abstractmethod
    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        pass

    @abstractmethod
    def close_task(self, todolist_key: UUID, task_key: UUID) -> None:
        pass

    @abstractmethod
    def get_raw_todolist(self, todolist_key: UUID) -> str:
        pass
