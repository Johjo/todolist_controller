from uuid import uuid4

import pytest
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase

from todolist_controller.controller import TodolistController
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.todolist_read_from_memory.todolist_read_from_memory import TodolistReadFromMemory
from todolist_controller.usage import UuidGeneratorRandom
from todolist_controller.uuid_generator_queue import UuidGeneratorQueue


def test_give_no_task_when_task_is_empty(sut: TodolistReadFromMemory) -> None:
    actual = sut.get_task(task_key=uuid4())
    assert actual is None


def test_give_no_task_when_todolist_is_newly_created(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController) -> None:
    controller.create_todolist()

    actual = sut.get_task(task_key=uuid4())
    assert actual is None


def test_give_task_when_todolist_one_task_is_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")

    actual = sut.get_task(task_key=task_one_key)
    assert actual == TaskPresentation(key=task_one_key, name="buy the milk", is_opened=True)


def test_give_task_when_task_is_closed(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")
    controller.close_task(task_key=task_one_key)

    actual = sut.get_task(task_key=task_one_key)
    assert actual == TaskPresentation(key=task_one_key, name="buy the milk", is_opened=False)


@pytest.fixture
def uuid_generator() -> UuidGeneratorRandom:
    return UuidGeneratorRandom()

@pytest.fixture
def sut(event_store: EventStoreInMemory) -> TodolistReadFromMemory:
    return TodolistReadFromMemory(event_store=event_store)

@pytest.fixture
def controller(uuid_generator: UuidGeneratorQueue, sut: TodolistReadFromMemory,
               event_store: EventStoreInMemory) -> TodolistController:
    return TodolistController(uuid_generator=uuid_generator,
                                    todolist=TodolistUseCase(event_store=event_store), event_store=None,
                                    todolist_read=sut)

@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()