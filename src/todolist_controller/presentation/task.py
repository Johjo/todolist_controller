from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, eq=True)
class TaskPresentation:
    key:  UUID
    name: str
    events: list[Any] | None = None
