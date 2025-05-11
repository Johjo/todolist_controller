from uuid import uuid4

from todolist_hexagon.events import TodoListCreated, Event
from todolist_hexagon.base.events import EventList

from tests.fixture import NOW
from tests.test_todolist_controller.fixture import TodolistReadForTest
from todolist_controller.controller import TodolistController


def test_give_nothing_when_aggregate_does_not_exist(sut: TodolistController, todolist_read: TodolistReadForTest) -> None:
    aggregate_key = uuid4()

    expected : EventList[Event] = []

    todolist_read.feed_event(aggregate_key, expected)

    assert sut.get_events(aggregate_key=aggregate_key) == expected


def test_give_events(sut: TodolistController, todolist_read: TodolistReadForTest) -> None:
    aggregate_key = uuid4()
    expected : EventList[Event] = [TodoListCreated(when=NOW)]
    todolist_read.feed_event(aggregate_key, expected)
    actual = sut.get_events(aggregate_key=aggregate_key)

    assert actual == expected


