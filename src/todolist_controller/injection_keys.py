from pyqure import Key
from todolist_hexagon.todolist_usecase import TodolistUseCasePort

from todolist_controller.port import TodolistReadPort
from todolist_controller.primary_port import TodolistControllerPort
from todolist_controller.secondary_port import UuidGeneratorPort

UUID_GENERATOR: Key[UuidGeneratorPort] = Key(UuidGeneratorPort.__name__, UuidGeneratorPort)
TODOLIST_USE_CASE: Key[TodolistUseCasePort] = Key(TodolistUseCasePort.__name__, TodolistUseCasePort)
TODOLIST_QUERY: Key[TodolistReadPort] = Key(TodolistReadPort.__name__, TodolistReadPort)
TODOLIST_CONTROLLER: Key[TodolistControllerPort] = Key(TodolistControllerPort.__name__, TodolistControllerPort)
TODOLIST_DB_NAME : Key[str] = Key("todolist-db-name", str)
TODOLIST_DB_USER : Key[str] = Key("todolist-db-user", str)
TODOLIST_DB_PASSWORD : Key[str] = Key("todolist-db-password", str)
TODOLIST_DB_HOST : Key[str] = Key("todolist-db-host", str)
TODOLIST_DB_PORT : Key[int] = Key("todolist-db-port", int)
