from uuid import UUID

from todolist_hexagon.base.events import EventList
from todolist_hexagon.events import Event
from todolist_hexagon.base.ports import EventStorePort


class GetEventBuiltIn:
    def __init__(self, event_store: EventStorePort[Event]) -> None:
        self._event_store = event_store

    def get_events(self, aggregate_key: UUID) -> EventList[Event]:
        return self._event_store.events_for(key=aggregate_key)
