from todolist_hexagon.ports import EventStorePort

from todolist_controller.controller import TodolistReadPort
from todolist_controller.todolist_read_from_event_store.get_events import GetEventBuiltIn
from todolist_controller.todolist_read_from_event_store.get_task import GetTaskBuiltIn
from todolist_controller.todolist_read_from_event_store.get_todolist import GetTodolistBuiltIn


class TodolistReadFromEventStore(GetEventBuiltIn, GetTodolistBuiltIn, GetTaskBuiltIn, TodolistReadPort):
    def __init__(self, event_store: EventStorePort):
        super().__init__(event_store)

