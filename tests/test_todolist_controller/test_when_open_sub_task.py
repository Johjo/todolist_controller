from uuid import uuid4

from tests.test_todolist_controller.fixture import UuidGeneratorForTest, TodolistUseCaseForTest, OpenSubTask
from todolist_controller.primary_port import TodolistControllerPort


def test_create_task_via_use_case_when_open_sub_task(uuid_generator: UuidGeneratorForTest,
                                                     todolist_use_case: TodolistUseCaseForTest,
                                                     sut: TodolistControllerPort) -> None:
    expected = OpenSubTask(parent_task_key=(uuid4()), children_task_key=uuid4(), title="buy the milk",
                           description="description")
    uuid_generator.feed(expected.children_task_key)

    sut.open_sub_task(parent_task_key=expected.parent_task_key, title=expected.title, description=expected.description)

    assert todolist_use_case.history() == [expected]


def test_give_children_task_key_when_open_sub_task(uuid_generator: UuidGeneratorForTest,
                                                   sut: TodolistControllerPort) -> None:
    expected = OpenSubTask(parent_task_key=uuid4(), children_task_key=uuid4(), title="buy the milk",
                           description="description")
    uuid_generator.feed(expected.children_task_key)

    actual = sut.open_sub_task(parent_task_key=expected.parent_task_key, title=expected.title,
                               description=expected.description)

    assert actual == expected.children_task_key
