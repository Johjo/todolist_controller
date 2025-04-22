from dataclasses import dataclass
from uuid import UUID


@dataclass
class Task:
    key: UUID
    name: str

@dataclass
class TodolistPresentation:
    tasks: list[Task]
