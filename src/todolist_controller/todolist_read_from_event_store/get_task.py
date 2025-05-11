from uuid import UUID

from todolist_hexagon.events import TaskOpened, TaskDescribed, TaskClosed, SubTaskAttached, Event
from todolist_hexagon.base.ports import EventStorePort

from todolist_controller.presentation.task import TaskPresentation, SubTask


class GetTaskBuiltIn:
    def __init__(self, event_store: EventStorePort[Event]) -> None:
        self._event_store = event_store

    def _task_presentation(self, task_key: UUID) -> TaskPresentation | None:
        task_is_opened = None
        task_title = None
        subtask_keys: list[UUID] = []
        for event in self._event_store.events_for(task_key):
            match event:
                case TaskOpened():
                    task_is_opened = True

                case TaskClosed():
                    task_is_opened = False

                case TaskDescribed(title=title, description=description):
                    task_title = title

                case SubTaskAttached(task_key=children_task_key):
                    subtask_keys.append(children_task_key)

                case _:
                    raise Exception(f"Event {event} not implemented")

        if task_title is None or task_is_opened is None:
            return None
        return TaskPresentation(key=task_key, name=task_title, is_opened=task_is_opened,
                                subtasks=list(map(self._sub_task_presentation, subtask_keys)))

    def _sub_task_presentation(self, task_key: UUID) -> SubTask:
        task_title = ""
        is_opened = False
        for event in self._event_store.events_for(task_key):
            match event:
                case TaskDescribed(title=title, description=description):
                    task_title = title
                case TaskOpened():
                    is_opened = True
                case SubTaskAttached():
                    pass
                case _:
                    raise Exception(f"Event {event} not implemented")

        return SubTask(key=task_key, name=task_title, is_opened=is_opened)


    def get_task(self, task_key: UUID) -> TaskPresentation | None:
        return self._task_presentation(task_key=task_key)

    def __task_keys(self, parent_task_key: UUID) -> list[UUID]:
        todolist_events = self._event_store.events_for(key=parent_task_key)
        task_keys = None
        for event in todolist_events:
            match event:
                case TaskDescribed():
                    task_keys = []
                case TaskOpened() | TaskClosed():
                    pass
                case SubTaskAttached(task_key=task_key):
                    task_keys.append(task_key)
                case _:
                    raise Exception(f"Event {event} is not implemented")
        return task_keys
