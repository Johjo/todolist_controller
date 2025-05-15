import logging
from typing import cast
from uuid import UUID

from todolist_hexagon.base.ports import EventStorePort
from todolist_hexagon.events import TodoListCreated, TaskAttached, Event, TaskEvent

from todolist_controller.presentation.sub_task import SubTask
from todolist_controller.presentation.todolist import TodolistPresentation
from todolist_controller.todolist_read_from_event_store.get_sub_task import get_sub_task

logger = logging.getLogger(__name__)

class GetTodolistBuiltIn:
    def __init__(self, event_store: EventStorePort[Event]):
        self._event_store = event_store

    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation:
        task_keys = self.__task_keys(todolist_key=todolist_key)
        if task_keys is None:
            return None
        return TodolistPresentation(key=todolist_key, tasks=[self.__task_presentation_or_default(task_key) for task_key in task_keys])

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
                    logger.error(f"Event {event} not implemented")

        return task_keys

    def __task_presentation_or_default(self, task_key: UUID) -> SubTask:
        events = cast(list[TaskEvent], self._event_store.events_for(task_key))
        task = get_sub_task(task_key=task_key, events=events)
        return task if task is not None else SubTask(key=task_key, name="?", is_opened=False)


