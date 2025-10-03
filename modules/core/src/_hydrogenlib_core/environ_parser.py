import os
from typing import Union

from .typefunc import get_type_name

origin_environ = None

ENV_ORIGIN = 0x1
ENV_NEW = 0x2


def init():
    """
    这个操作将会完全影响模块的运作初始值
    """
    global origin_environ
    origin_environ = os.environ.copy()
    return Environment()


def _split_env_string(string):
    if os.name == 'nt':
        value = string.split(';')
    elif os.name == 'posix':
        value = string.split(':')
    elif os.name == 'java':
        value = string.split(':')
    else:
        raise NotImplementedError(f"{os.name} is not supported")
    return value


class EnvironmentItem:
    __slots__ = ('name', 'value')

    def __init__(self, name, value):
        # print(name)
        self.name = name
        self.value = value

    def set_value(self, value):
        self.value = value

    def copy(self):
        return EnvironmentItem(self.name, self.value)


ITEM_TYPE = Union[str, EnvironmentItem]


class EnvironmentVarieble(str):
    def __new__(cls, *args, **kwargs):
        cls = super().__new__(cls)
        return cls

    def __init__(self, name, value_string, split_char=';'):
        self.name = name
        self.split_char = split_char
        self.value = [EnvironmentItem(name, v) for v in _split_env_string(value_string)]

    def append(self, item: ITEM_TYPE):
        if isinstance(item, str):
            item = EnvironmentItem(self.name, item)
        self.value.append(item)

    def remove(self, item: ITEM_TYPE):
        if isinstance(item, str):
            item = EnvironmentItem(self.name, item)
        self.value.remove(item)

    def index(self, item: ITEM_TYPE):
        if isinstance(item, str):
            item = EnvironmentItem(self.name, item)
        return self.value.index(item)

    def pop(self, index: int):
        return self.value.pop(index)

    def copy(self):
        var = EnvironmentVarieble(self.name, '')
        var.value = self.value.copy()
        return var

    def __contains__(self, item: ITEM_TYPE):
        if isinstance(item, str):
            item = EnvironmentItem(self.name, item)
        return item in self.value

    def __len__(self):
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]

    def __setitem__(self, index, value):
        self.value[index].set_value(value)

    def __iter__(self):
        yield from self.value

    def __str__(self):
        return f'{self.split_char.join([str(v.value) for v in self.value])}'

    __repr__ = __str__


class Environment:
    __slots__ = ('env',)

    def __to_env_dict(self, env):
        result = {}
        for key, value in env._instances():
            if isinstance(value, EnvironmentVarieble):
                result[key] = value
            else:
                result[key] = EnvironmentVarieble(key, value)
        return result

    def __init__(self, env=None):
        if env is None:
            env = os.environ
        elif isinstance(env, Environment):
            env = env.env
        elif isinstance(env, int):
            if env == ENV_ORIGIN:
                env = origin_environ
            elif env == ENV_NEW:
                env = {}
            else:
                raise ValueError(f"{env} is not a valid value")
            env = origin_environ
        else:
            env = dict(env)

        self.env = self.__to_env_dict(env)

    def copy(self):
        return Environment(self.env)

    def keys(self):
        return self.env.keys()

    def values(self):
        return map(str, self.env.values())

    def items(self):
        return map(lambda x: (x[0], str(x[1])), self.env.items())

    def __getitem__(self, key):
        # if inspect.stack()[2].function == 'activate':  # 处理 activate 函数 ( os.update ) 不支持自定义的类型
        #     return str(self.env[key])
        return self.env[key]

    def __setitem__(self, key, value):
        self.env[key] = value

    def __delitem__(self, key):
        del self.env[key]

    def __contains__(self, key):
        return key in self.env

    def __str__(self):
        return f'{get_type_name(self)}({self.env})'

    __repr__ = __str__


class _ManagerEnvironmentItem:
    __slots__ = ('name', 'env')

    def __init__(self, name, value):
        if isinstance(value, str):
            value = EnvironmentVarieble(name, value)
            value = Environment({name: value})

        self.name, self.env = name, value

    def __getitem__(self, item):
        return self.env[item]

    def __setitem__(self, item, value):
        self.env[item] = value

    def __delitem__(self, item):
        del self.env[item]

    @classmethod
    def from_environ(cls, name, *args, **kwargs):
        env = Environment(*args, **kwargs)
        return cls(name, env)

    def copy(self):
        return _ManagerEnvironmentItem(self.name, self.env.copy())

    def activate(self):
        os.environ.update(self.env)

    def avtivate_all(self):
        os.environ.clear()
        self.activate()

    def __str__(self):
        return "Item-" + str(self.env)

    __repr__ = __str__


class EnvironmentManager:
    __slots__ = ('_env',)

    def __init__(self, env_mapping=None):
        if env_mapping is not None:
            self._env: dict[str, _ManagerEnvironmentItem] = {
                k: _ManagerEnvironmentItem(k, v) for k, v in env_mapping._instances()}
        else:
            self._env = {}

    def create_environ(self, name: str, clone_from=None):
        if clone_from is None:
            self._env[name] = _ManagerEnvironmentItem.from_environ(name, os.environ)
        elif isinstance(clone_from, str):
            origin_env = self._env[clone_from]
            self._env[name] = origin_env.copy()
        elif isinstance(clone_from, Environment):
            origin_env = clone_from
            self._env[name] = _ManagerEnvironmentItem(name, origin_env.copy())
        elif isinstance(clone_from, int):
            if clone_from == ENV_ORIGIN:
                self._env[name] = _ManagerEnvironmentItem.from_environ(name, origin_environ)
            elif clone_from == ENV_NEW:
                self._env[name] = _ManagerEnvironmentItem.from_environ(name, {})
            else:
                raise ValueError(f"{clone_from} is not a valid value")
        else:
            raise TypeError(f"{clone_from} is not Envionment item")

    def add_environ(self, name: str, value):
        # 如果Value是Item类型,那么就直接赋值
        # 否则进行类型转换
        self._env[name] = _ManagerEnvironmentItem(name, value) if not isinstance(value,
                                                                                 _ManagerEnvironmentItem) else value

    def env(self, key: str = None, k=None, v=None) -> Union[
        dict[str, _ManagerEnvironmentItem], _ManagerEnvironmentItem]:
        if key is None:  # 返回所有环境变量
            return self._env
        else:
            if k is None:  # 当 k 为 None 时,返回环境变量字典
                return self._env[key]
            elif v is not None:  # 当 k 和 v 都不为 None 时,修改环境变量字典
                self._env[key][k] = v

    def activate(self, key: str):
        self._env[key].activate()

    def activate_all(self, key: str):
        self._env[key].avtivate_all()

    def __getitem__(self, key: str):
        return self._env[key]

    def __setitem__(self, key: str, value):
        if isinstance(value, str):
            value = EnvironmentVarieble(key, value)
            value = Environment({key: value})
            value = _ManagerEnvironmentItem(key, value)

        elif isinstance(value, Environment):
            value = _ManagerEnvironmentItem(key, value)

        elif isinstance(value, EnvironmentVarieble):
            value = Environment({key: value})
            value = _ManagerEnvironmentItem(key, value)

        if not isinstance(value, _ManagerEnvironmentItem):
            raise TypeError(f"{value} is not Envionment item")

        self._env[key] = value

    def __delitem__(self, key: str):
        del self._env[key]
