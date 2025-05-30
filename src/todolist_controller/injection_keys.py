from pyqure import Key
from todolist_hexagon.todolist_usecase import TodolistUseCasePort

from todolist_controller.port import TodolistReadPort
from todolist_controller.primary_port import TodolistControllerPort
from todolist_controller.secondary_port import UuidGeneratorPort

UUID_GENERATOR: Key[UuidGeneratorPort] = Key("uuid generator", UuidGeneratorPort)
TODOLIST_USE_CASE: Key[TodolistUseCasePort] = Key("uuid generator", TodolistUseCasePort)
TODOLIST_QUERY: Key[TodolistReadPort] = Key("uuid generator", TodolistReadPort)
TODOLIST_CONTROLLER: Key[TodolistControllerPort] = Key(TodolistControllerPort.__name__, TodolistControllerPort)