from uuid import uuid4

from tests.test_todolist_controller.fixture import UuidGeneratorForTest, TodolistUseCaseForTest, OpenTask, CloseTask
from todolist_controller.controller import TodolistController


def test_close_task_via_use_case_when_close_task(uuid_generator: UuidGeneratorForTest,
                                                   todolist_use_case: TodolistUseCaseForTest,
                                                   sut: TodolistController) -> None:
    task_key = uuid4()
    expected = CloseTask(task_key=task_key)

    sut.close_task(task_key=task_key)

    assert todolist_use_case.history() == [expected]