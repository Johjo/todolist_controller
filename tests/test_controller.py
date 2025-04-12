from abc import abstractmethod, ABC
from dataclasses import dataclass
from uuid import UUID, uuid4

import pytest

from todolist_controller.controller_port import TaskPresentation
from todolist_controller.controller import TodolistController


class TodolistGatewayPort(ABC):
    @abstractmethod
    def open_task(self, todolist_id: UUID, task_id: UUID, task_description: str) -> None:
        pass

    @abstractmethod
    def tasks(self, todolist_id: UUID) -> list[TaskPresentation]:
        pass


class UuidGeneratorPort(ABC):
    @abstractmethod
    def generate_uuid(self):
        pass


class UuidGeneratorForTest(UuidGeneratorPort):
    def __init__(self) -> None:
        self._next : UUID | None = None

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
    task_description: str


History = OpenTask


class TodolistGatewayForTest(TodolistGatewayPort):
    def __init__(self) -> None:
        self._tasks: dict[UUID, list[TaskPresentation]] = {}
        self._history: list[History] = []

    def open_task(self, todolist_id: UUID, task_id: UUID, task_description: str) -> None:
        self._history.append(OpenTask(todolist_id=todolist_id, task_id=task_id, task_description=task_description))

    def tasks(self, todolist_id: UUID) :
        return self._tasks[todolist_id]

    def history(self) -> list[History]:
        return self._history

    def feed(self, todolist_id: UUID, *tasks: TaskPresentation):
        self._tasks[todolist_id] = list(tasks)


@pytest.fixture
def uuid_generator() -> UuidGeneratorForTest:
    return UuidGeneratorForTest()


@pytest.fixture
def todolist_gateway() -> TodolistGatewayForTest:
    return TodolistGatewayForTest()


@pytest.fixture
def sut(uuid_generator: UuidGeneratorForTest, todolist_gateway: TodolistGatewayForTest) -> TodolistController:
    return TodolistController(uuid_generator, todolist_gateway)


def test_get_created_todolist_uuid_when_create_todolist(uuid_generator: UuidGeneratorForTest, sut: TodolistController):
    expected_todolist_id = uuid4()
    uuid_generator.feed(expected_todolist_id)

    todolist_id = sut.create_todolist()

    assert todolist_id == expected_todolist_id


def test_create_task_on_gateway_when_create_task(uuid_generator: UuidGeneratorForTest,
                                                 todolist_gateway: TodolistGatewayForTest, sut: TodolistController):
    expected = OpenTask(todolist_id=(uuid4()), task_id=uuid4(), task_description="buy the milk")
    uuid_generator.feed(expected.task_id)

    sut.open_task(todolist_id=expected.todolist_id, task_description=expected.task_description)

    assert todolist_gateway.history() == [expected]


def test_give_task_id_when_create_task(uuid_generator: UuidGeneratorForTest,
                                       todolist_gateway: TodolistGatewayForTest, sut: TodolistController):
    expected = OpenTask(todolist_id=(uuid4()), task_id=uuid4(), task_description="buy the milk")
    uuid_generator.feed(expected.task_id)

    actual = sut.open_task(todolist_id=expected.todolist_id, task_description=expected.task_description)

    assert actual == expected.task_id


def test_give_all_tasks(sut: TodolistController, todolist_gateway: TodolistGatewayForTest):
    todolist_id = uuid4()
    expected = [TaskPresentation(uuid=uuid4(), name="buy the milk"), TaskPresentation(uuid=uuid4(), name="eat something")]
    todolist_gateway.feed(todolist_id, *expected)

    assert sut.get_tasks(todolist_id=todolist_id) == expected
