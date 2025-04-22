from uuid import UUID

from todolist_hexagon.events import TaskOpened, TaskDescribed, TaskClosed
from todolist_hexagon.ports import EventStorePort

from todolist_controller.presentation.task import TaskPresentation


class GetTaskBuiltIn:
    def __init__(self, event_store: EventStorePort) -> None:
        self._event_store = event_store

    def _task_presentation(self, task_key: UUID) -> TaskPresentation | None:
        task_presentation = None

        task_is_opened = None
        task_title = None

        for event in self._event_store.events_for(task_key):
            match event:
                case TaskOpened():
                    task_is_opened = True

                case TaskClosed():
                    task_is_opened = False

                case TaskDescribed(title=title, description=description):
                    task_title = title

                case _:
                    raise Exception(f"Event {event} not implemented")

        if task_title is None or task_is_opened is None:
            return None

        return TaskPresentation(key=task_key, name=task_title, is_opened=task_is_opened)


    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        return self._task_presentation(task_key=task_key)
