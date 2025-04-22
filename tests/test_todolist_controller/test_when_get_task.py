from uuid import uuid4

from tests.test_todolist_controller.fixture import TodolistReadForTest
from todolist_controller.controller import TodolistController
from todolist_controller.presentation.task import TaskPresentation


def test_give_task(sut: TodolistController, todolist_read: TodolistReadForTest) -> None:
    expected = TaskPresentation(key=uuid4(), name=f"buy the milk {uuid4()}")
    todolist_read.feed_task(expected.key, expected)

    actual = sut.get_task(task_key=expected.key)
    assert actual == expected
