import psycopg2
from todolist_hexagon.adapter_contract_testing.base_test_event_store import BaseTestEventStore
from todolist_hexagon.base.ports import EventStorePort
from todolist_hexagon.events import Event
from todolist_controller.todolist.secondary.event_store_pgsql import EventStorePgsql


class TestEventStorePgsql(BaseTestEventStore):
    def _sut(self) -> EventStorePort[Event]:
        connection = self.connect_to_pgsql()
        self.clean_events_table(connection)
        return EventStorePgsql(connection=connection)

    @staticmethod
    def clean_events_table(connection: psycopg2.extensions.connection) -> None:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM todolist.events")
        connection.commit()

    @staticmethod
    def connect_to_pgsql() -> psycopg2.extensions.connection:
        return psycopg2.connect(
            dbname="todolist_db",
            user="postgres",
            password="mysecretpassword",
            host="localhost",  # ou l'adresse de votre serveur PostgreSQL
            port=5432  # le port par défaut
        )
