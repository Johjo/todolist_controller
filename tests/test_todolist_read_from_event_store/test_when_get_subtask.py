from uuid import UUID, uuid4

import pytest
from todolist_hexagon.events import TaskOpened, TaskDescribed, TaskEvent, TaskClosed, SubTaskAttached

from tests.fixture import NOW
from todolist_controller.todolist_read_from_event_store.get_sub_task import get_sub_task
from todolist_controller.presentation.sub_task import SubTask

TASK_KEY = UUID("00000000-0000-0000-0000-000000000000")


@pytest.mark.parametrize("events,expected", [
    ([], None),
    ([TaskOpened(when=NOW)], SubTask(key=TASK_KEY, name="", is_opened=True)),
    ([SubTaskAttached(task_key=uuid4(), when=NOW)], SubTask(key=TASK_KEY, name="", is_opened=False)),
    ([TaskDescribed(title="buy the milk", description="at super market", when=NOW)], SubTask(key=TASK_KEY, name="buy the milk", is_opened=False)),
    ([TaskDescribed(title="buy the milk", description="at super market", when=NOW), TaskDescribed(title=None, description="at super market", when=NOW)], SubTask(key=TASK_KEY, name="buy the milk", is_opened=False)),
    ([TaskOpened(when=NOW), TaskClosed(when=NOW)], SubTask(key=TASK_KEY, name="", is_opened=False)),
    ([TaskOpened(when=NOW), TaskDescribed(title="buy the milk", description="at super market", when=NOW)]
     , SubTask(key=TASK_KEY, name="buy the milk", is_opened=True)),

])
def test_give_no_task_when_task_is_empty(events: list[TaskEvent], expected: SubTask | None) -> None:
    assert get_sub_task(task_key=TASK_KEY, events=events) == expected
