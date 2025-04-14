from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from todolist_controller.secondary_port import TodolistUseCasePort, UuidGeneratorPort
from todolist_controller.primary_port import TodolistControllerPort, TaskPresentation


class TodolistReadPort(ABC):
    @abstractmethod
    def tasks(self, todolist_id: UUID) -> list[TaskPresentation]:
        pass


class TodolistController(TodolistControllerPort):
    def __init__(self, uuid_generator: UuidGeneratorPort, todolist: TodolistUseCasePort, todolist_read: TodolistReadPort) -> None:
        self._in_todolist = todolist
        self._uuid_generator : UuidGeneratorPort = uuid_generator
        self._from_todolist = todolist_read

    def create_todolist(self) -> UUID:
        return self._uuid_generator.generate_uuid()

    def open_task(self, todolist_id: UUID, task_description: str) -> UUID:
        task_id : UUID = self._uuid_generator.generate_uuid()
        self._in_todolist.open_task(todolist_id=todolist_id, task_id=task_id,
                                    task_description=task_description)

        return task_id


    def get_tasks(self, todolist_id: UUID) -> List[TaskPresentation]:
        return self._from_todolist.tasks(todolist_id=todolist_id)

    def get_task(self, todolist_id: UUID, task_id: UUID) -> TaskPresentation | None:
        raise NotImplementedError()

    def close_task(self, todolist_id: UUID, task_id: UUID) -> None:
        raise NotImplementedError()
