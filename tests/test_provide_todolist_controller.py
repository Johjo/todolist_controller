from pyqure import PyqureMemory, pyqure

import todolist_controller.injection_keys as keys
from todolist_controller.dependencies import provide_todolist_controller


def test_provide_todolist_controller() -> None:
    dependencies: PyqureMemory = {}

    (provide, inject) = pyqure(dependencies)

    provide(keys.TODOLIST_DB_NAME, "todolist_db")
    provide(keys.TODOLIST_DB_USER, "postgres")
    provide(keys.TODOLIST_DB_PASSWORD, "mysecretpassword")
    provide(keys.TODOLIST_DB_HOST, "localhost")
    provide(keys.TODOLIST_DB_PORT, 5432)

    provide_todolist_controller(dependencies)

    assert inject(keys.TODOLIST_CONTROLLER) is not None


