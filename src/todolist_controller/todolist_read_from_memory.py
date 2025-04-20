from uuid import UUID

from todolist_hexagon.events import TaskOpened, TaskDescribed, TodoListCreated, TaskAttached
from todolist_hexagon.ports import EventStorePort

from todolist_controller.controller import TodolistReadPort
from todolist_controller.primary_port import TaskPresentation


class TodolistReadFromMemory(TodolistReadPort):
    def __init__(self, event_store: EventStorePort):
        self._event_store = event_store

    def tasks(self, todolist_key: UUID) -> list[TaskPresentation]:
        task_keys = self._task_keys(todolist_key=todolist_key)
        return [self._task_presentation(task_key=task_key) for task_key in task_keys]

    def _task_presentation(self, task_key: UUID) -> TaskPresentation:
        task_presentation = TaskPresentation(uuid=task_key, name="?")

        for event in self._event_store.events_for(task_key):
            match event:
                case TaskOpened():
                    pass
                case TaskDescribed(title=title, description=description):
                    task_presentation = TaskPresentation(uuid=task_key, name=title)
                case _:
                    raise Exception(f"Event {event} not implemented")

        return task_presentation

    def _task_keys(self, todolist_key: UUID) -> list[UUID]:
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
