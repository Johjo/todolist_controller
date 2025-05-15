from uuid import uuid4

import pytest
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory

from todolist_controller.controller import TodolistController
from todolist_controller.presentation.task import TaskPresentation
from todolist_controller.presentation.sub_task import SubTask
from todolist_controller.todolist_read_from_event_store.todolist_read_from_event_store import TodolistReadFromEventStore
from todolist_controller.usage import UuidGeneratorRandom


def test_give_no_task_when_task_is_empty(sut: TodolistReadFromEventStore) -> None:
    actual = sut.get_task(task_key=uuid4())
    assert actual is None


def test_give_no_task_when_todolist_is_newly_created(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromEventStore, controller: TodolistController) -> None:
    controller.create_todolist()

    actual = sut.get_task(task_key=uuid4())
    assert actual is None


def test_give_task_when_todolist_one_task_is_attached(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromEventStore, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")

    actual = sut.get_task(task_key=task_one_key)
    assert actual == TaskPresentation(key=task_one_key, name="buy the milk", is_opened=True, subtasks=[])


def test_give_task_when_task_is_closed(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromEventStore, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_one_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")
    controller.close_task(task_key=task_one_key)

    actual = sut.get_task(task_key=task_one_key)
    assert actual == TaskPresentation(key=task_one_key, name="buy the milk", is_opened=False, subtasks=[])

def test_give_task_when_sub_task_is_opened(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromEventStore, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    parent_task_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")

    task_key_one = controller.open_sub_task(parent_task_key=parent_task_key, title="do something", description="somewhere")

    actual = sut.get_task(task_key=parent_task_key)
    assert actual == TaskPresentation(key=parent_task_key, name="buy the milk", is_opened=True, subtasks=[SubTask(key=task_key_one, name="do something", is_opened=True)])

def test_give_task_when_sub_sub_task_is_opened(uuid_generator: UuidGeneratorRandom, sut: TodolistReadFromEventStore, controller: TodolistController, event_store: EventStoreInMemory) -> None:
    todolist_key = controller.create_todolist()
    task_key = controller.open_task(todolist_key=todolist_key, title="buy the milk", description="at super market")

    sub_task = controller.open_sub_task(parent_task_key=task_key, title="do something", description="somewhere")
    controller.open_sub_task(parent_task_key=sub_task, title="do something else", description="where ?")

    actual = sut.get_task(task_key=task_key)
    assert actual == TaskPresentation(key=task_key, name="buy the milk", is_opened=True, subtasks=[SubTask(key=sub_task, name="do something", is_opened=True)])


@pytest.fixture
def uuid_generator() -> UuidGeneratorRandom:
    return UuidGeneratorRandom()

@pytest.fixture
def sut(event_store: EventStoreInMemory) -> TodolistReadFromEventStore:
    return TodolistReadFromEventStore(event_store=event_store)

@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()