from dataclasses import dataclass
from typing import Self
from uuid import UUID

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


def test_xxx_when_yyy():
    todolist = Todolist()

    assert todolist.uncommitted_event == ()