import pytest
from datetime_provider import DateTimeProviderDeterministic
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase

from tests.fixture import NOW
from todolist_controller.controller import TodolistController
from todolist_controller.todolist_read_from_event_store.todolist_read_from_event_store import TodolistReadFromEventStore
from todolist_controller.usage import UuidGeneratorRandom
from todolist_controller.uuid_generator_queue import UuidGeneratorQueue


@pytest.fixture
def uuid_generator() -> UuidGeneratorRandom:
    return UuidGeneratorRandom()


@pytest.fixture
def datetime_provider() -> DateTimeProviderDeterministic:
    datetime_provider = DateTimeProviderDeterministic()
    datetime_provider.feed(NOW)
    return datetime_provider


@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()


@pytest.fixture
def controller(uuid_generator: UuidGeneratorQueue, sut: TodolistReadFromEventStore,
               event_store: EventStoreInMemory, datetime_provider: DateTimeProviderDeterministic) -> TodolistController:
    return TodolistController(uuid_generator=uuid_generator,
                              todolist=TodolistUseCase(event_store=event_store, datetime_provider=datetime_provider),
                              todolist_read=sut)
