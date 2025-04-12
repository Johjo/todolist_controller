from typing import List
from uuid import UUID

from tests.test_controller import UuidGeneratorPort, TodolistGatewayPort
from todolist_controller.controller_port import TodolistControllerPort, TaskPresentation


class TodolistController(TodolistControllerPort):
    def __init__(self, uuid_generator: UuidGeneratorPort, todolist_gateway: TodolistGatewayPort) -> None:
        self._todolist_gateway = todolist_gateway
        self._uuid_generator : UuidGeneratorPort = uuid_generator

    def create_todolist(self) -> UUID:
        return self._uuid_generator.generate_uuid()

    def open_task(self, todolist_id: UUID, task_description: str) -> UUID:
        task_id = self._uuid_generator.generate_uuid()
        self._todolist_gateway.open_task(todolist_id=todolist_id, task_id=task_id,
                                         task_description=task_description)

        return task_id


    def get_tasks(self, todolist_id: UUID) -> List[TaskPresentation]:
        return self._todolist_gateway.tasks(todolist_id=todolist_id)

    def get_task(self, todolist_id: UUID, task_id: UUID) -> TaskPresentation | None:
        raise NotImplementedError()

    def close_task(self, todolist_id: UUID, task_id: UUID) -> None:
        raise NotImplementedError()
