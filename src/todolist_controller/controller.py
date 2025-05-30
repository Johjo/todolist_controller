from uuid import UUID

from todolist_hexagon.base.events import EventList
from todolist_hexagon.events import Event
from todolist_hexagon.todolist_usecase import TodolistUseCasePort

from todolist_controller.injection_keys import UUID_GENERATOR, TODOLIST_USE_CASE, TODOLIST_QUERY
from todolist_controller.port import TodolistReadPort
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation
from todolist_controller.primary_port import TodolistControllerPort
from todolist_controller.secondary_port import UuidGeneratorPort
from pyqure import PyqureMemory, pyqure


class TodolistController(TodolistControllerPort):
    def __init__(self, dependencies: PyqureMemory) -> None:
        (_, inject) = pyqure(dependencies)

        self._in_todolist : TodolistUseCasePort = inject(TODOLIST_USE_CASE)
        self._uuid_generator : UuidGeneratorPort = inject(UUID_GENERATOR)
        self._from_todolist : TodolistReadPort = inject(TODOLIST_QUERY)

    def create_todolist(self) -> UUID:
        todolist_key = self._uuid_generator.generate_uuid()
        self._in_todolist.create_todolist(todolist_key=todolist_key)
        return todolist_key

    def open_task(self, todolist_key: UUID, title: str, description: str) -> UUID:
        task_key : UUID = self._uuid_generator.generate_uuid()
        self._in_todolist.open_task(todolist_key=todolist_key, task_key=task_key,
                                    title=title, description=description)

        return task_key

    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation | None:
        return self._from_todolist.get_todolist(todolist_key=todolist_key)


    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        return self._from_todolist.get_task(task_key=task_key)

    def close_task(self, task_key: UUID) -> None:
        self._in_todolist.close_task(task_key=task_key)

    def get_events(self, aggregate_key: UUID) -> EventList[Event]:
        return self._from_todolist.get_events(aggregate_key=aggregate_key)

    def open_sub_task(self, parent_task_key: UUID, title: str, description: str) -> UUID:
        children_task_key = self._uuid_generator.generate_uuid()
        self._in_todolist.open_sub_task(parent_task_key=parent_task_key,
                                        children_task_key=children_task_key, title=title,
                                        description=description)
        return children_task_key

    def describe_task(self, task_key: UUID, title: str | None, description: str | None) -> None:
        self._in_todolist.describe_task(task_key=task_key, title=title, description=description)

