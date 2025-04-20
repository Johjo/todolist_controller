from uuid import uuid4

import pytest

from todolist_controller.uuid_generator_queue import UuidGeneratorQueue


def test_tell_when_generator_is_empty() -> None:
    with pytest.raises(Exception) as e:
        UuidGeneratorQueue().generate_uuid()

    assert "uuid generator is empty" in str(e.value)


def test_give_feed_uuid_when_call_generator() -> None:
    generator = UuidGeneratorQueue()
    uuid1 = uuid4()
    uuid2 = uuid4()
    uuid3 = uuid4()
    generator.feed(uuid1, uuid2, uuid3)
    assert generator.generate_uuid() == uuid1
    assert generator.generate_uuid() == uuid2
    assert generator.generate_uuid() == uuid3


