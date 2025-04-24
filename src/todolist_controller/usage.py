from uuid import UUID, uuid4

from datetime_provider import DateTimeProvider
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase

from todolist_controller.controller import TodolistController
from todolist_controller.primary_port import TodolistControllerPort
from todolist_controller.secondary_port import UuidGeneratorPort
from todolist_controller.todolist_read_from_memory.todolist_read_from_memory import TodolistReadFromMemory

event_store = EventStoreInMemory()

def create_todolist_controller() -> TodolistControllerPort:
    return TodolistController(uuid_generator=UuidGeneratorRandom(),
                              todolist=TodolistUseCase(event_store=event_store, datetime_provider=DateTimeProvider()), todolist_read=TodolistReadFromMemory(event_store), event_store=event_store)


class UuidGeneratorRandom(UuidGeneratorPort):
    def generate_uuid(self) -> UUID:
        return uuid4()

