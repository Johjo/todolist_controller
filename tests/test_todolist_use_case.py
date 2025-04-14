from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from todolist_controller.secondary_port import TodolistUseCasePort


class TodolistUseCase(TodolistUseCasePort):
    def open_task(self, todolist_id: UUID, task_id: UUID, task_description: str) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class TaskOpened:
    todolist_id: UUID
    task_id: UUID
    task_name: str

Event = TaskOpened



@dataclass(frozen=True, eq=True)
class Todolist:
    uncommitted_event: tuple[Event, ...] = ()
    def open_task(self) -> Self:
        pass

    def decide(self, command):
        event = (TaskOpened(todolist_id=command.todolist_id, task_id=command.task_id, task_name=command.task_name),)
        return Todolist(uncommitted_event=self.uncommitted_event + event)


def test_nothing_append_when_when_do_nothing():
    todolist = Todolist()
    assert todolist.uncommitted_event == ()


@dataclass()
class OpenTask:
    todolist_id: UUID
    task_id: UUID
    task_name: str


def test_task_opened_when_open_task():
    command = any_open_task_command()

    todolist = Todolist()
    actual = todolist.decide(command)
    assert actual.uncommitted_event == (
    TaskOpened(todolist_id=command.todolist_id, task_id=command.task_id, task_name=command.task_name),)


def test_two_tasks_opened_when_open_two_tasks():
    first_command = any_open_task_command()
    second_command = any_open_task_command()

    todolist = Todolist()
    actual = todolist.decide(first_command)
    actual = actual.decide(second_command)

    assert actual.uncommitted_event == (
        TaskOpened(todolist_id=first_command.todolist_id,
                   task_id=first_command.task_id,
                   task_name=first_command.task_name),
        TaskOpened(todolist_id=second_command.todolist_id,
                   task_id=second_command.task_id,
                   task_name=second_command.task_name),
    )



def any_open_task_command():
    todolist_id = uuid4()
    task_id = uuid4()
    task_name = f"todo {uuid4()}"
    command = OpenTask(todolist_id=todolist_id, task_id=task_id, task_name=task_name)
    return command
