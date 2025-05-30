from dataclasses import dataclass
from uuid import UUID

from todolist_hexagon.base.events import EventList
from todolist_hexagon.events import Event
from todolist_hexagon.result import Result, Ok
from todolist_hexagon.todolist_usecase import TodolistUseCasePort
from todolist_hexagon.task_error import TaskNotFound, TaskError
from todolist_controller.port import TodolistReadPort
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.todolist import TodolistPresentation
from todolist_controller.secondary_port import UuidGeneratorPort


class TodolistReadForTest(TodolistReadPort):
    def __init__(self) -> None:
        self._events: dict[UUID, EventList[Event]] = {}
        self._todolist: dict[UUID, TodolistPresentation | None] = {}
        self._tasks: dict[UUID, TaskPresentation] = {}


    def get_todolist(self, todolist_key: UUID) -> TodolistPresentation | None:
        return self._todolist[todolist_key]

    def feed_task(self, task_key: UUID, task_presentation: TaskPresentation) -> None:
        self._tasks[task_key] = task_presentation

    def feed_todolist(self, todolist_key: UUID, todolist: TodolistPresentation | None) -> None:
        self._todolist[todolist_key] = todolist

    def get_task(self, task_key: UUID) -> TaskPresentation:
        return self._tasks[task_key]

    def feed_event(self, aggregate_key: UUID, expected: EventList[Event]) -> None:
        self._events[aggregate_key] = expected

    def get_events(self, aggregate_key: UUID) -> EventList[Event]:
        return self._events[aggregate_key]


class UuidGeneratorForTest(UuidGeneratorPort):
    def __init__(self) -> None:
        self._next: UUID | None = None

    def feed(self, next_uuid: UUID) -> None:
        self._next = next_uuid

    def generate_uuid(self) -> UUID:
        if self._next is None:
            raise Exception("next uuid not fed")

        return self._next


@dataclass
class OpenTask:
    todolist_key: UUID
    task_key: UUID
    title: str
    description: str


@dataclass
class OpenSubTask:
    parent_task_key: UUID
    children_task_key: UUID
    title: str
    description: str

@dataclass
class DescribeTask:
    task_key: UUID
    title: str | None
    description: str | None


@dataclass
class CreateTodolist:
    todolist_key: UUID


@dataclass
class CloseTask:
    task_key: UUID


History = OpenTask | CreateTodolist | CloseTask | OpenSubTask | DescribeTask


class TodolistUseCaseForTest(TodolistUseCasePort):
    def __init__(self) -> None:
        self._tasks: dict[UUID, TodolistPresentation] = {}
        self._history: list[History] = []

    def create_todolist(self, todolist_key: UUID) -> None:
        self._history.append(CreateTodolist(todolist_key=todolist_key))

    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        self._history.append(OpenTask(todolist_key=todolist_key, task_key=task_key, title=title, description=description))

    def open_sub_task(self, parent_task_key: UUID, children_task_key: UUID, title: str, description: str) -> None:
        self._history.append(
            OpenSubTask(parent_task_key=parent_task_key, children_task_key=children_task_key, title=title,
                        description=description))

    def close_task(self, task_key: UUID) -> Result[None, TaskError]:
        self._history.append(CloseTask(task_key=task_key))
        return Ok(None)

    def describe_task(self, *, task_key: UUID, title: str | None = None, description: str | None = None) -> Result[
        None, TaskError]:
        self._history.append(DescribeTask(task_key=task_key, title=title, description=description))
        return Ok(None)

    def tasks(self, todolist_key: UUID) -> TodolistPresentation:
        return self._tasks[todolist_key]

    def history(self) -> list[History]:
        return self._history
