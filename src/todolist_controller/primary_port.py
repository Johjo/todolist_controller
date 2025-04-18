from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID



@dataclass(frozen=True, eq=True)
class TaskPresentation:
    uuid:  UUID
    name: str


class TodolistControllerPort:
    @abstractmethod
    def create_todolist(self) -> UUID:
        pass

    @abstractmethod
    def open_task(self, todolist_key: UUID, title: str, description: str) -> UUID:
        pass

    @abstractmethod
    def get_tasks(self, todolist_key: UUID) -> List[TaskPresentation]:
        pass

    @abstractmethod
    def get_task(self, todolist_key: UUID, task_key: UUID) -> TaskPresentation | None:
        pass

    @abstractmethod
    def close_task(self, todolist_key: UUID, task_key: UUID) -> None:
        pass

    @abstractmethod
    def get_raw_todolist(self, todolist_key: UUID) -> str:
        pass
