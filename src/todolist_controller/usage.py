from uuid import UUID, uuid4

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
        return uuid4()


class EventStoreInMemory(EventStorePort):
    def save(self, *aggregate_event: AggregateEvent) -> None:
        print(aggregate_event)

    def events_for(self, key: UUID) -> EventList:
        raise NotImplementedError()


class TodolistRead(TodolistReadPort):
    def tasks(self, todolist_key: UUID) -> list[TaskPresentation]:
        print("TodolistRead not implemented")
        return []


