from .field import Field
from .container import AnnoationSupportContainerBase, validator_mark, update_fields_attrs
from .file_opener import FileOpener
from .abstract_model import AbstractModel
from .abstract_backend import AbstractBackend
from .config_metadata import *
from .type_registry import *

from .global_ import *

global_registry.register(
    AbstractModel,
    object,
    lambda x: x.as_dict()
)
