from dataclasses import dataclass
from uuid import UUID, uuid4

import pytest
from todolist_hexagon.todolist_usecase import TodolistUseCasePort

from todolist_controller.controller import TodolistController, TodolistReadPort
from todolist_controller.primary_port import TaskPresentation
from todolist_controller.secondary_port import UuidGeneratorPort


class UuidGeneratorForTest(UuidGeneratorPort):
    def __init__(self) -> None:
        self._next: UUID | None = None

    def feed(self, next_uuid: UUID) -> None:
        self._next = next_uuid

    def generate_uuid(self) -> UUID:
        if self._next is None:
            raise Exception("next uuid not fed")

        return self._next


@dataclass
class OpenTask:
    todolist_id: UUID
    task_id: UUID
    title: str
    description: str


@dataclass
class CreateTodolist:
    todolist_key: UUID


History = OpenTask | CreateTodolist


class TodolistReadForTest(TodolistReadPort):
    def __init__(self) -> None:
        self._todolist: dict[UUID, list[TaskPresentation]] = {}

    def tasks(self, todolist_id: UUID) -> list[TaskPresentation]:
        return self._todolist[todolist_id]

    def feed(self, todolist_id: UUID, *tasks: TaskPresentation) -> None:
        self._todolist[todolist_id] = list(tasks)


class TodolistUseCaseForTest(TodolistUseCasePort):
    def __init__(self) -> None:
        self._tasks: dict[UUID, list[TaskPresentation]] = {}
        self._history: list[History] = []

    def create_todolist(self, key: UUID) -> None:
        self._history.append(CreateTodolist(todolist_key=key))

    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        self._history.append(OpenTask(todolist_id=todolist_key, task_id=task_key, title=title, description=description))

    def tasks(self, todolist_id: UUID) -> list[TaskPresentation]:
        return self._tasks[todolist_id]

    def history(self) -> list[History]:
        return self._history

    def feed(self, todolist_id: UUID, *tasks: TaskPresentation) -> None:
        self._tasks[todolist_id] = list(tasks)


def test_get_created_todolist_uuid_when_create_todolist(uuid_generator: UuidGeneratorForTest,
                                                        sut: TodolistController) -> None:
    expected_todolist_id = uuid4()
    uuid_generator.feed(expected_todolist_id)

    todolist_id = sut.create_todolist()

    assert todolist_id == expected_todolist_id


def test_create_todolist_via_use_case_when_create_todolist(uuid_generator: UuidGeneratorForTest,
                                                           todolist_use_case: TodolistUseCaseForTest,
                                                           sut: TodolistController) -> None:
    todolist_key = uuid4()
    uuid_generator.feed(todolist_key)

    sut.create_todolist()
    todolist_use_case.create_todolist(key=todolist_key)

    assert todolist_use_case.history() == [CreateTodolist(todolist_key=todolist_key)]


def test_create_task_via_use_case_when_create_task(uuid_generator: UuidGeneratorForTest,
                                                   todolist_use_case: TodolistUseCaseForTest,
                                                   sut: TodolistController) -> None:
    expected = OpenTask(todolist_id=(uuid4()), task_id=uuid4(), title="buy the milk", description="description")
    uuid_generator.feed(expected.task_id)

    sut.open_task(todolist_id=expected.todolist_id, title=expected.title, description=expected.description)

    assert todolist_use_case.history() == [expected]


def test_give_task_id_when_create_task(uuid_generator: UuidGeneratorForTest, sut: TodolistController) -> None:
    expected = OpenTask(todolist_id=(uuid4()), task_id=uuid4(), title="buy the milk", description="description")
    uuid_generator.feed(expected.task_id)

    actual = sut.open_task(todolist_id=expected.todolist_id, title=expected.title, description=expected.description)

    assert actual == expected.task_id


def test_give_all_tasks(sut: TodolistController, todolist_read: TodolistReadForTest) -> None:
    todolist_id = uuid4()
    expected = [TaskPresentation(uuid=uuid4(), name="buy the milk"),
                TaskPresentation(uuid=uuid4(), name="eat something")]
    todolist_read.feed(todolist_id, *expected)

    assert sut.get_tasks(todolist_id=todolist_id) == expected


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
