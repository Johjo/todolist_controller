from uuid import UUID

from todolist_hexagon.events import EventList
from todolist_hexagon.ports import EventStorePort


class GetEventBuiltIn:
    def __init__(self, event_store: EventStorePort) -> None:
        self._event_store = event_store

    def get_events(self, aggregate_key: UUID) -> EventList:
        return self._event_store.events_for(key=aggregate_key)
