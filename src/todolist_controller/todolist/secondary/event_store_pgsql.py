import json
from typing import Any
from uuid import UUID

import psycopg2
from todolist_hexagon.events import EventList, EventBase, TaskOpened, TaskClosed, TodoListCreated, TaskDescribed, \
    TaskAttached, Event, SubTaskAttached
from todolist_hexagon.ports import EventStorePort, AggregateEvent


class EventStorePgsql(EventStorePort):
    def __init__(self, connection: psycopg2.extensions.connection) -> None:
        self.conn = connection

    def save(self, *aggregate_events: AggregateEvent) -> None:
        cursor = self.conn.cursor()

        for one_aggregate_event in aggregate_events:
            for one_event in one_aggregate_event.events:
                cursor.execute(
                    "INSERT INTO todolist.events (key, event_name, payload, publication_date) VALUES (%s, %s, %s, %s)",
                    (str(one_aggregate_event.key), one_event.__class__.__name__, self._serialize(one_event), one_event.when))
        self.conn.commit()

    def events_for(self, key: UUID) -> EventList:
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, event_name, payload, publication_date FROM todolist.events WHERE key = %s", (str(key),))
        return [self._to_event(row) for row in cursor.fetchall()]

    def _serialize(self, event: EventBase) -> str:
        match event:
            case TaskOpened() | TaskClosed() | TodoListCreated():
                return json.dumps({})
            case TaskDescribed(title=title, description=description):
                return json.dumps({"title": title, "description": description})
            case TaskAttached(task_key=task_key) | SubTaskAttached(task_key=task_key):
                return json.dumps({"task_key": str(task_key)})
            case _:
                raise NotImplementedError(event)

    def _to_event(self, row: Any) -> Event:
        when = row[3]
        payload = json.loads(row[2])
        match row[1]:
            case "TaskOpened":
                return TaskOpened(when=when)
            case "TaskDescribed":
                return TaskDescribed(title=payload["title"], description=payload["description"], when=when)
            case "TaskClosed":
                return TaskClosed(when=when)
            case "TodoListCreated":
                return TodoListCreated(when=when)
            case "TaskAttached":
                return TaskAttached(task_key=UUID(payload["task_key"]), when=when)
            case "SubTaskAttached":
                return SubTaskAttached(task_key=UUID(payload["task_key"]), when=when)
            case _:
                raise NotImplementedError(row[1])
