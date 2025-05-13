from abc import abstractmethod
from uuid import UUID

from todolist_hexagon.base.events import EventList
from todolist_hexagon.events import Event
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
    def open_sub_task(self, parent_task_key: UUID, title: str, description: str) -> UUID:
        pass

    @abstractmethod
    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation | None:
        pass

    @abstractmethod
    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        pass

    @abstractmethod
    def close_task(self, task_key: UUID) -> None:
        pass

    @abstractmethod
    def get_events(self, aggregate_key: UUID) -> EventList[Event]:
        pass

    @abstractmethod
    def describe_task(self, task_key : UUID, title: str | None, description: str | None) -> None:
        pass
