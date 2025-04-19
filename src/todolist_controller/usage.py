from uuid import UUID, uuid4

from todolist_hexagon.events import EventList
from todolist_hexagon.ports import EventStorePort, AggregateEvent
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase

from todolist_controller.controller import TodolistController, TodolistReadPort
from todolist_controller.primary_port import TaskPresentation, TodolistControllerPort
from todolist_controller.secondary_port import UuidGeneratorPort


event_store = EventStoreInMemory()

def create_todolist_controller() -> TodolistControllerPort:
    return TodolistController(uuid_generator=UuidGeneratorRandom(),
                              todolist=TodolistUseCase(event_store=event_store), todolist_read=TodolistRead(), event_store=event_store)


class UuidGeneratorRandom(UuidGeneratorPort):
    def generate_uuid(self) -> UUID:
        return uuid4()



class TodolistRead(TodolistReadPort):
    def tasks(self, todolist_key: UUID) -> list[TaskPresentation]:
        print("TodolistRead not implemented")
        return []


