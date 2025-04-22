from uuid import UUID

from todolist_hexagon.events import TaskOpened, TaskDescribed, TodoListCreated, TaskAttached
from todolist_hexagon.ports import EventStorePort

from todolist_controller.controller import TodolistReadPort
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation
from todolist_controller.todolist_read_from_memory_bis.get_todolist import GetTodolistBuiltIn


class TodolistReadFromMemory(GetTodolistBuiltIn, TodolistReadPort):
    def __init__(self, event_store: EventStorePort):
        super().__init__(event_store)
        self._event_store = event_store

    def _task_presentation_or_default(self, task_key : UUID) -> TaskPresentation:
        task = self._task_presentation(task_key=task_key)
        return task if task is not None else TaskPresentation(key=task_key, name="?")

    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        return self._task_presentation(task_key=task_key)

    def _task_presentation(self, task_key: UUID) -> TaskPresentation | None:
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

