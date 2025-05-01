import pytest

from tests.test_todolist_controller.fixture import UuidGeneratorForTest, TodolistUseCaseForTest, TodolistReadForTest
from todolist_controller.controller import TodolistController


@pytest.fixture
def sut(uuid_generator: UuidGeneratorForTest, todolist_use_case: TodolistUseCaseForTest,
        todolist_read: TodolistReadForTest) -> TodolistController:
    return TodolistController(uuid_generator, todolist_use_case, todolist_read)


@pytest.fixture
def uuid_generator() -> UuidGeneratorForTest:
    return UuidGeneratorForTest()


@pytest.fixture
def todolist_use_case() -> TodolistUseCaseForTest:
    return TodolistUseCaseForTest()


@pytest.fixture
def todolist_read() -> TodolistReadForTest:
    return TodolistReadForTest()
