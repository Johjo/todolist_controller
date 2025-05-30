import pytest
from datetime_provider import DateTimeProviderDeterministic
from pyqure import pyqure, PyqureMemory
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase

from tests.fixture import NOW
from todolist_controller.controller import TodolistController
from todolist_controller.injection_keys import UUID_GENERATOR, TODOLIST_USE_CASE, TODOLIST_QUERY
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

    memory: PyqureMemory = {}
    (provide, inject) = pyqure(memory)
    provide(UUID_GENERATOR, uuid_generator)
    provide(TODOLIST_USE_CASE, TodolistUseCase(event_store=event_store, datetime_provider=datetime_provider))
    provide(TODOLIST_QUERY, sut)

    return TodolistController(dependencies=memory)
