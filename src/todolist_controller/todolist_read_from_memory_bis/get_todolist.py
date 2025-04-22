from uuid import UUID

from todolist_hexagon.events import TodoListCreated, TaskAttached
from todolist_hexagon.ports import EventStorePort

from todolist_controller.presentation.todolist import TodolistPresentation


class GetTodolistBuiltIn:
    def __init__(self, event_store: EventStorePort):
        self._event_store = event_store

    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation:
        task_keys = self.__task_keys(todolist_key=todolist_key)
        return [self._task_presentation_or_default(task_key) for task_key in task_keys]

    def __task_keys(self, todolist_key: UUID) -> list[UUID]:
        todolist_events = self._event_store.events_for(key=todolist_key)
        task_keys : list[UUID] = []
        for event in todolist_events:
            match event:
                case TodoListCreated():
                    pass
                case TaskAttached(task_key=task_key):
                    task_keys.append(task_key)
                    pass
                case _:
                    raise Exception(f"Event {event} is not implemented")
        return task_keys
