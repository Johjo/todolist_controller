from uuid import uuid4

from tests.test_todolist_controller.fixture import UuidGeneratorForTest, TodolistUseCaseForTest, CreateTodolist
from todolist_controller.controller import TodolistController


def test_get_created_todolist_uuid_when_create_todolist(uuid_generator: UuidGeneratorForTest,
                                                        sut: TodolistController) -> None:
    expected_todolist_key = uuid4()
    uuid_generator.feed(expected_todolist_key)

    todolist_key = sut.create_todolist()

    assert todolist_key == expected_todolist_key


def test_create_todolist_via_use_case_when_create_todolist(uuid_generator: UuidGeneratorForTest,
                                                           todolist_use_case: TodolistUseCaseForTest,
                                                           sut: TodolistController) -> None:
    todolist_key = uuid4()
    uuid_generator.feed(todolist_key)

    sut.create_todolist()

    assert todolist_use_case.history() == [CreateTodolist(todolist_key=todolist_key)]
