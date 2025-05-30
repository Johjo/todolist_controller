from abc import ABC, abstractmethod
from uuid import UUID

from todolist_hexagon.base.events import EventList
from todolist_hexagon.events import Event

from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation


class TodolistReadPort(ABC):
    @abstractmethod
    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation | None:
        pass

    @abstractmethod
    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        pass

    @abstractmethod
    def get_events(self, aggregate_key: UUID) -> EventList[Event]:
        pass
