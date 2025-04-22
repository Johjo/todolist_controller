from uuid import UUID

from todolist_hexagon.events import TaskOpened, TaskDescribed
from todolist_hexagon.ports import EventStorePort

from todolist_controller.presentation.task import TaskPresentation


class GetTaskBuiltIn:
    def __init__(self, event_store: EventStorePort) -> None:
        self._event_store = event_store

    def _task_presentation(self, task_key: UUID) -> TaskPresentation | None:
        task_presentation = None

        for event in self._event_store.events_for(task_key):
            match event:
                case TaskOpened():
                    pass
                case TaskDescribed(title=title, description=description):
                    task_presentation = TaskPresentation(key=task_key, name=title, events=None)
                case _:
                    raise Exception(f"Event {event} not implemented")

        return task_presentation

    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        return self._task_presentation(task_key=task_key)
