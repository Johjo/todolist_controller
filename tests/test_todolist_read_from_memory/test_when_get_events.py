from uuid import uuid4

import pytest
from todolist_hexagon.events import TaskDescribed, TaskOpened, TodoListCreated
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase

from tests.fixture import NOW
from todolist_controller.controller import TodolistController
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.todolist_read_from_memory.todolist_read_from_memory import TodolistReadFromMemory
from todolist_controller.usage import UuidGeneratorRandom
from todolist_controller.uuid_generator_queue import UuidGeneratorQueue


def test_give_no_event(sut: TodolistReadFromMemory) -> None:
    actual = sut.get_events(aggregate_key=uuid4())
    assert actual == []


def test_give_event_when_todolist_is_newly_created(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController) -> None:
    todolist_key = controller.create_todolist()

    actual = sut.get_events(aggregate_key=todolist_key)
    assert actual == [TodoListCreated(when=NOW)]



def test_give_task_when_todolist_one_task_is_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")

    actual = sut.get_events(aggregate_key=task_one_key)
    assert actual == [TaskDescribed(title="buy the milk", description="at super market", when=NOW), TaskOpened(when=NOW)]


# @pytest.mark.skip
# def test_give_two_tasks_when_todolist_two_task_are_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromMemory, controller: TodolistController, event_store: EventStoreInMemory) -> None:
#     todolist_key = controller.create_todolist()
#     task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")
#     task_two_key = controller.open_task(todolist_key=todolist_key, title="buy the water", description="at home")
#
#     todolist = sut.get_todolist(todolist_key=todolist_key)
#     assert todolist == TodolistPresentation(tasks=[Task(key=task_one_key, name="buy the milk"), Task(key=task_two_key, name="buy the water")])





    # tasks = sut.tasks(todolist_key=todolist_key)
    # assert tasks == []

@pytest.fixture
def uuid_generator() -> UuidGeneratorRandom:
    return UuidGeneratorRandom()

@pytest.fixture
def sut(event_store: EventStoreInMemory) -> TodolistReadFromMemory:
    return TodolistReadFromMemory(event_store=event_store)


@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()