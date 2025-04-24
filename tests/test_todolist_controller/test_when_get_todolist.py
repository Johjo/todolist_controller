from uuid import uuid4

from tests.test_todolist_controller.fixture import TodolistReadForTest
from todolist_controller.controller import TodolistController
from todolist_controller.presentation.todolist import TodolistPresentation, Task


def test_give_nothing_when_todolist_does_not_exist(sut: TodolistController, todolist_read: TodolistReadForTest) -> None:
    todolist_key = uuid4()
    expected = None

    todolist_read.feed_todolist(todolist_key, expected)

    assert sut.get_todolist(todolist_key=todolist_key) == expected


def test_give_todolist(sut: TodolistController, todolist_read: TodolistReadForTest) -> None:
    todolist_key = uuid4()
    expected = TodolistPresentation(key = todolist_key, tasks=[
        Task(key=uuid4(), name="buy the milk", is_opened=True),
        Task(key=uuid4(), name="eat something", is_opened=True)])

    todolist_read.feed_todolist(todolist_key, expected)

    assert sut.get_todolist(todolist_key=todolist_key) == expected

