from .type_registry import *

global_registry = TypeRegistry()
global_convertor = TypeConvertor(global_registry)

global_convertor.set_default(
    lambda data, target: target(data)
)
