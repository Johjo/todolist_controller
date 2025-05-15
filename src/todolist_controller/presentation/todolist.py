from dataclasses import dataclass
from uuid import UUID

from todolist_controller.presentation.sub_task import SubTask


@dataclass
class TodolistPresentation:
    key: UUID
    tasks: list[SubTask]
