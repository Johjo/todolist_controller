from uuid import UUID

from todolist_controller.secondary_port import UuidGeneratorPort


class UuidGeneratorQueue(UuidGeneratorPort):
    def __init__(self) -> None:
        self._uuids : list[UUID] = []

    def generate_uuid(self) -> UUID:
        if not self._uuids:
            raise Exception("uuid generator is empty")
        return self._uuids.pop(0)

    def feed(self, *uuid: UUID) -> None:
        self._uuids.extend(uuid)
