from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=True)
class SubTask:
    key:  UUID
    name: str
    is_opened: bool
