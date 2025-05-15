from dataclasses import replace, dataclass
from typing import assert_never
from uuid import UUID

from todolist_hexagon.events import TaskEvent, TaskOpened, TaskDescribed, TaskClosed, SubTaskAttached

from todolist_controller.presentation.sub_task import SubTask


def get_sub_task(task_key: UUID, events: list[TaskEvent]) -> SubTask | None:
    if not events:
        return None

    sub_task = SubTask(key=task_key, name="", is_opened=False)

    for event in events:
        match event:
            case TaskOpened():
                sub_task = replace(sub_task, is_opened=True)
            case TaskDescribed(title=title, description=description):
                if title:
                    sub_task = replace(sub_task, name=title)
            case TaskClosed():
                sub_task = replace(sub_task, is_opened=False)
            case SubTaskAttached():
                pass
            case _:
                assert_never(event)
    return sub_task
