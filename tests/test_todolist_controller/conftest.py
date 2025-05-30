import pytest

from tests.test_todolist_controller.fixture import UuidGeneratorForTest, TodolistUseCaseForTest, TodolistReadForTest
from todolist_controller.controller import TodolistController
from pyqure import pyqure, PyqureMemory

from todolist_controller.injection_keys import UUID_GENERATOR, TODOLIST_USE_CASE, TODOLIST_QUERY


@pytest.fixture
def sut(uuid_generator: UuidGeneratorForTest, todolist_use_case: TodolistUseCaseForTest,
        todolist_read: TodolistReadForTest) -> TodolistController:

    memory: PyqureMemory = {}
    (provide, inject) = pyqure(memory)
    provide(UUID_GENERATOR, uuid_generator)
    provide(TODOLIST_USE_CASE, todolist_use_case)
    provide(TODOLIST_QUERY, todolist_read)

    return TodolistController(dependencies=memory)


@pytest.fixture
def uuid_generator() -> UuidGeneratorForTest:
    return UuidGeneratorForTest()


@pytest.fixture
def todolist_use_case() -> TodolistUseCaseForTest:
    return TodolistUseCaseForTest()


@pytest.fixture
def todolist_read() -> TodolistReadForTest:
    return TodolistReadForTest()
