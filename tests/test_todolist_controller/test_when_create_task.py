from uuid import uuid4

from tests.test_todolist_controller.fixture import UuidGeneratorForTest, TodolistUseCaseForTest, OpenTask
from todolist_controller.controller import TodolistController


def test_create_task_via_use_case_when_create_task(uuid_generator: UuidGeneratorForTest,
                                                   todolist_use_case: TodolistUseCaseForTest,
                                                   sut: TodolistController) -> None:
    expected = OpenTask(todolist_key=(uuid4()), task_key=uuid4(), title="buy the milk", description="description")
    uuid_generator.feed(expected.task_key)

    sut.open_task(todolist_key=expected.todolist_key, title=expected.title, description=expected.description)

    assert todolist_use_case.history() == [expected]


def test_give_task_key_when_create_task(uuid_generator: UuidGeneratorForTest, sut: TodolistController) -> None:
    expected = OpenTask(todolist_key=(uuid4()), task_key=uuid4(), title="buy the milk", description="description")
    uuid_generator.feed(expected.task_key)

    actual = sut.open_task(todolist_key=expected.todolist_key, title=expected.title, description=expected.description)

    assert actual == expected.task_key
