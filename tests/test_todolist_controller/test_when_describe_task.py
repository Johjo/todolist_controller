from uuid import uuid4

from tests.test_todolist_controller.fixture import UuidGeneratorForTest, TodolistUseCaseForTest, DescribeTask
from todolist_controller.primary_port import TodolistControllerPort


def test_create_task_via_use_case_when_describe_task(uuid_generator: UuidGeneratorForTest,
                                                     todolist_use_case: TodolistUseCaseForTest,
                                                     sut: TodolistControllerPort) -> None:
    expected = DescribeTask(task_key=uuid4(), title="buy the milk", description="description")

    sut.describe_task(task_key=expected.task_key, title=expected.title, description=expected.description)

    assert todolist_use_case.history() == [expected]
