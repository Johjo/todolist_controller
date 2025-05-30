import psycopg2
from datetime_provider import DateTimeProvider
from pyqure import PyqureMemory, pyqure
from todolist_hexagon.todolist_usecase import TodolistUseCase

from todolist_controller import injection_keys as keys, TodolistController
from todolist_controller.todolist.secondary.event_store_pgsql import EventStorePgsql
from todolist_controller.todolist_read_from_event_store.todolist_read_from_event_store import TodolistReadFromEventStore
from todolist_controller.usage import UuidGeneratorRandom


def provide_todolist_controller(dependencies: PyqureMemory) -> None:
    (provide, inject) = pyqure(dependencies)

    event_store = EventStorePgsql(connection=psycopg2.connect(
        dbname=inject(keys.TODOLIST_DB_NAME),
        user=inject(keys.TODOLIST_DB_USER),
        password=inject(keys.TODOLIST_DB_PASSWORD),
        host=inject(keys.TODOLIST_DB_HOST),
        port=inject(keys.TODOLIST_DB_PORT)
    ))
    provide(keys.UUID_GENERATOR, UuidGeneratorRandom())
    provide(keys.TODOLIST_USE_CASE, TodolistUseCase(datetime_provider=DateTimeProvider(), event_store=event_store))
    provide(keys.TODOLIST_QUERY, TodolistReadFromEventStore(event_store=event_store))
    provide(keys.TODOLIST_CONTROLLER, TodolistController(dependencies=dependencies))
