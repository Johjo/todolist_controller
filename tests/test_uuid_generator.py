from uuid import UUID

from todolist_controller.usage import UuidGeneratorRandom


def test_generate_uuid() -> None:
    uuid_generator = UuidGeneratorRandom()
    assert isinstance(uuid_generator.generate_uuid(), UUID)

def test_generate_always_different_value() -> None:
    uuid_generator = UuidGeneratorRandom()
    assert uuid_generator.generate_uuid() != uuid_generator.generate_uuid()