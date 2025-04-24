from dataclasses import dataclass
from uuid import UUID


@dataclass
class Task:
    key: UUID
    name: str
    is_opened: bool

@dataclass
class TodolistPresentation:
    key: UUID
    tasks: list[Task]
