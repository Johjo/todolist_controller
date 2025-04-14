from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from todolist_controller.secondary_port import TodolistUseCasePort


class TodolistUseCase(TodolistUseCasePort):
    def open_task(self, todolist_id: UUID, task_id: UUID, task_description: str) -> None:
        raise NotImplementedError


class Event:
    pass


@dataclass(frozen=True, eq=True)
class Todolist:
    uncommitted_event: tuple[Event] = ()
    def open_task(self) -> Self:
        pass

    def decide(self, command):
        return Todolist(uncommitted_event=(TaskOpened, ))


def test_nothing_append_when_when_do_nothing():
    todolist = Todolist()
    assert todolist.uncommitted_event == ()


@dataclass()
class OpenTask:
    todolist_id: UUID

@dataclass(frozen=True)
class TaskOpened:
    pass


def test_task_opened_when_open_task():
    todolist = Todolist()
    todolist_id = uuid4()
    actual = todolist.decide(OpenTask(todolist_id=todolist_id))
    assert actual.uncommitted_event == (TaskOpened, )
