from uuid import UUID

from todolist_hexagon.events import TodoListCreated, TaskAttached, TaskOpened, TaskDescribed
from todolist_hexagon.ports import EventStorePort

from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation


class GetTodolistBuiltIn:
    def __init__(self, event_store: EventStorePort):
        self._event_store = event_store

    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation:
        task_keys = self.__task_keys(todolist_key=todolist_key)
        if task_keys is None:
            return None
        return [self.__task_presentation_or_default(task_key) for task_key in task_keys]

    def __task_keys(self, todolist_key: UUID) -> list[UUID]:
        todolist_events = self._event_store.events_for(key=todolist_key)
        task_keys = None
        for event in todolist_events:
            match event:
                case TodoListCreated():
                    task_keys = []
                case TaskAttached(task_key=task_key):
                    task_keys.append(task_key)
                    pass
                case _:
                    raise Exception(f"Event {event} is not implemented")
        return task_keys

    def __task_presentation_or_default(self, task_key : UUID) -> TaskPresentation:
        task = self.__task_presentation(task_key=task_key)
        return task if task is not None else TaskPresentation(key=task_key, name="?")

    def __task_presentation(self, task_key: UUID) -> TaskPresentation | None:
        task_presentation = None

        for event in self._event_store.events_for(task_key):
            match event:
                case TaskOpened():
                    pass
                case TaskDescribed(title=title, description=description):
                    task_presentation = TaskPresentation(key=task_key, name=title, events=None)
                case _:
                    raise Exception(f"Event {event} not implemented")

        return task_presentation

