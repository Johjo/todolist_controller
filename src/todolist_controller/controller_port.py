from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID



@dataclass
class TaskPresentation:
    uuid:  UUID
    name: str


class TodolistControllerPort:
    @abstractmethod
    def create_todolist(self) -> UUID:
        pass

    @abstractmethod
    def open_task(self, todolist_uuid: UUID, task_description: str) -> UUID:
        pass

    @abstractmethod
    def get_tasks(self, todolist_uuid: UUID) -> List[TaskPresentation]:
        pass

    @abstractmethod
    def get_task(self, todolist_uuid: UUID, task_uuid: UUID) -> Optional[TaskPresentation]:
        pass

    @abstractmethod
    def close_task(self, todolist_uuid: UUID, task_uuid: UUID) -> None:
        pass
