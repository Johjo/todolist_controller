from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCasePort

from todolist_controller.secondary_port import UuidGeneratorPort
from todolist_controller.primary_port import TodolistControllerPort, TaskPresentation


class TodolistReadPort(ABC):
    @abstractmethod
    def tasks(self, todolist_key: UUID) -> list[TaskPresentation]:
        pass


class TodolistController(TodolistControllerPort):
    def __init__(self, uuid_generator: UuidGeneratorPort, todolist: TodolistUseCasePort, todolist_read: TodolistReadPort, event_store: EventStoreInMemory) -> None:
        self._in_todolist = todolist
        self._uuid_generator : UuidGeneratorPort = uuid_generator
        self._from_todolist = todolist_read
        self._event_store = event_store

    def create_todolist(self) -> UUID:
        todolist_key = self._uuid_generator.generate_uuid()
        self._in_todolist.create_todolist(key=todolist_key)
        return todolist_key

    def open_task(self, todolist_key: UUID, title: str, description: str) -> UUID:
        task_key : UUID = self._uuid_generator.generate_uuid()
        self._in_todolist.open_task(todolist_key=todolist_key, task_key=task_key,
                                    title=title, description=description)

        return task_key

    def get_tasks(self, todolist_key: UUID) -> List[TaskPresentation]:
        return self._from_todolist.tasks(todolist_key=todolist_key)


    def get_task(self, todolist_key: UUID, task_key: UUID) -> TaskPresentation | None:
        raise NotImplementedError()

    def close_task(self, todolist_key: UUID, task_key: UUID) -> None:
        raise NotImplementedError()

    def get_raw_todolist(self, todolist_key: UUID) -> str:
        return str(self._event_store.events_for(key=todolist_key))
