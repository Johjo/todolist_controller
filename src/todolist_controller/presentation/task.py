from dataclasses import dataclass
from uuid import UUID

from todolist_controller.presentation.sub_task import SubTask


@dataclass(frozen=True, eq=True)
class TaskPresentation:
    key:  UUID
    name: str
    is_opened: bool
    subtasks: list[SubTask]