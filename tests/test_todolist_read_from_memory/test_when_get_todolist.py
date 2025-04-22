from uuid import uuid4

import pytest
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase

from todolist_controller.controller import TodolistController
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.todolist_read_from_memory_bis.todolist_read_from_memory import TodolistReadFromMemory
from todolist_controller.usage import UuidGeneratorRandom
from todolist_controller.uuid_generator_queue import UuidGeneratorQueue


def test_give_no_task_when_task_is_empty(sut: TodolistReadFromMemory) -> None:
    tasks = sut.get_todolist(todolist_key=uuid4())
    assert tasks == []


def test_give_no_task_when_todolist_is_newly_created(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController) -> None:
    todolist_key = controller.create_todolist()

    tasks = sut.get_todolist(todolist_key=todolist_key)
    assert tasks == []



def test_give_one_task_when_todolist_one_task_is_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")

    tasks = sut.get_todolist(todolist_key=todolist_key)
    assert tasks == [TaskPresentation(key=task_one_key, name="buy the milk")]


def test_give_two_tasks_when_todolist_two_task_are_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")
    task_two_key = controller.open_task(todolist_key=todolist_key, title="buy the water", description="at home")

    tasks = sut.get_todolist(todolist_key=todolist_key)
    assert tasks == [TaskPresentation(key=task_one_key, name="buy the milk"), TaskPresentation(key=task_two_key, name="buy the water")]





    # tasks = sut.tasks(todolist_key=todolist_key)
    # assert tasks == []

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