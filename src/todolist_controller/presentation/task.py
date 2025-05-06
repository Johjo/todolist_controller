from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, eq=True)
class SubTask:
    key:  UUID
    name: str
    is_opened: bool

@dataclass(frozen=True, eq=True)
class TaskPresentation:
    key:  UUID
    name: str
    is_opened: bool
    subtasks: list[SubTask]