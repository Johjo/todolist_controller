from uuid import UUID, uuid4

import psycopg2
from datetime_provider import DateTimeProvider
from todolist_hexagon.todolist_usecase import TodolistUseCase

from todolist_controller.controller import TodolistController
from todolist_controller.injection_keys import UUID_GENERATOR, TODOLIST_USE_CASE, TODOLIST_QUERY
from todolist_controller.primary_port import TodolistControllerPort
from todolist_controller.secondary_port import UuidGeneratorPort
from todolist_controller.todolist.secondary.event_store_pgsql import EventStorePgsql
from pyqure import pyqure, PyqureMemory
from todolist_controller.todolist_read_from_event_store.todolist_read_from_event_store import TodolistReadFromEventStore


dependencies: PyqureMemory = {}
(provide, inject) = pyqure(dependencies)


def create_todolist_controller(*, db_name: str, db_user: str, db_password: str,
                               db_host: str, db_port: int) -> TodolistControllerPort:
    event_store = EventStorePgsql(connection=psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,  # ou l'adresse de votre serveur PostgreSQL
        port=db_port  # le port par défaut
    ))

    provide(UUID_GENERATOR, UuidGeneratorRandom())
    provide(TODOLIST_USE_CASE, TodolistUseCase(event_store=event_store, datetime_provider=DateTimeProvider()))
    provide(TODOLIST_QUERY, TodolistReadFromEventStore(event_store))

    return TodolistController(dependencies=dependencies)


class UuidGeneratorRandom(UuidGeneratorPort):
    def generate_uuid(self) -> UUID:
        return uuid4()

