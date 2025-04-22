from uuid import UUID

from todolist_hexagon.ports import EventStorePort

from todolist_controller.presentation.todolist import TodolistPresentation


class GetTodolistBuiltIn:
    def __init__(self, event_store: EventStorePort):
        self._event_store = event_store

    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation:
        task_keys = self._task_keys(todolist_key=todolist_key)
        return [self._task_presentation_or_default(task_key) for task_key in task_keys]
