from uuid import uuid4

import pytest
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory

from tests.test_todolist_read_from_memory.conftest import uuid_generator, event_store, controller
from todolist_controller.controller import TodolistController
from todolist_controller.presentation.todolist import TodolistPresentation, Task
from todolist_controller.todolist_read_from_memory.todolist_read_from_memory import TodolistReadFromMemory
from todolist_controller.usage import UuidGeneratorRandom


def test_give_no_task_when_task_is_empty(sut: TodolistReadFromMemory) -> None:
    todolist = sut.get_todolist(todolist_key=uuid4())
    assert todolist is None


def test_give_no_task_when_todolist_is_newly_created(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController) -> None:
    todolist_key = controller.create_todolist()

    actual = sut.get_todolist(todolist_key=todolist_key)
    assert actual == TodolistPresentation(key=todolist_key, tasks=[])



def test_give_one_task_when_todolist_one_task_is_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")

    actual = sut.get_todolist(todolist_key=todolist_key)
    assert actual == TodolistPresentation(key=todolist_key, tasks=[Task(key=task_one_key, name="buy the milk", is_opened=True)])


def test_give_todolist_when_task_is_closed(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")
    controller.close_task(task_key=task_one_key)

    actual = sut.get_todolist(todolist_key=todolist_key)
    assert actual == TodolistPresentation(key=todolist_key, tasks=[Task(key=task_one_key, name="buy the milk", is_opened=False)])


def test_give_two_tasks_when_todolist_two_task_are_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")
    task_two_key = controller.open_task(todolist_key=todolist_key, title="buy the water", description="at home")

    actual = sut.get_todolist(todolist_key=todolist_key)
    assert actual == TodolistPresentation(key=todolist_key, tasks=[Task(key=task_one_key, name="buy the milk", is_opened=True), Task(key=task_two_key, name="buy the water", is_opened=True)])







    # tasks = sut.tasks(todolist_key=todolist_key)
    # assert tasks == []


@pytest.fixture
def sut(event_store: EventStoreInMemory) -> TodolistReadFromMemory:
    return TodolistReadFromMemory(event_store=event_store)


