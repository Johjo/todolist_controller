from uuid import UUID

from todolist_hexagon.events import EventList
from todolist_hexagon.ports import EventStorePort, AggregateEvent
from todolist_hexagon.todolist_usecase import TodolistUseCase

from todolist_controller.controller import TodolistController, TodolistReadPort
from todolist_controller.primary_port import TaskPresentation, TodolistControllerPort
from todolist_controller.secondary_port import UuidGeneratorPort


def create_todolist_controller() -> TodolistControllerPort:
    return TodolistController(uuid_generator=UuidGeneratorRandom(),
                              todolist=TodolistUseCase(event_store=EventStoreInMemory()), todolist_read=TodolistRead())


class UuidGeneratorRandom(UuidGeneratorPort):
    def generate_uuid(self) -> UUID:
        raise NotImplementedError()


class EventStoreInMemory(EventStorePort):
    def save(self, *aggregate_event: AggregateEvent) -> None:
        pass

    def events_for(self, key: UUID) -> EventList:
        raise NotImplementedError()


class TodolistRead(TodolistReadPort):
    def tasks(self, todolist_id: UUID) -> list[TaskPresentation]:
        raise NotImplementedError()


