import logging

# module end 我们会将模块的很多常量慢慢集成到这里

zlibcon_logger = logging.getLogger(__name__)

# const var = [module id][error_const: 1, flag_const: 0, info_const: 2][code]

# flags
DBX_FUNC_TYPE_MRO = 0x1001
DBX_FUNC_TYPE_GET = 0x1002

# flags
ETY_TYPE_KEY = 0x1003
ETY_TYPE_IV = 0x1004

# error
BCR_EXIST_NAME = 0x3101
BCR_NAME_NOT_FOUND = 0x3102
BCR_CANNOT_FOUND = 0x3103
BCR_BAD_REQUEST = 0x3104

# flags
BCR_PERSON = 0x3004
BCR_GROUP = 0x3005
BCR_ALL = 0x3006
BCR_RANGE = 0x3007

BCR_SEND = 0x3008
BCR_OPERATOR = 0x3009

# operation flags
BCR_DISCONNECT = 0x3001

PERM_ROLE_ALLOW = 0x4000
PERM_ROLE_DENY = 0x4001

JSON_DECODE = 0x5001
JSON_ENCODE = 0x5002

UNKNOWN = "Unknown"  # ???

_link_constants = []


def link_constant(name, value):
    """
    create new constant in `libcon`


    :param name:
    :param value:
    :return:
    """
    globals()[name] = value
    _link_constants.append(name)


def unlink_constant(name):
    if name not in _link_constants:
        raise ValueError(f"{name} is not a constant")
    del globals()[name]


zlibcon_logger.debug("Module zlibcon loading ...")
