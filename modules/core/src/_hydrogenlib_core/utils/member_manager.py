from typing import Union

from ..utils.auto import AutoRegDict, AutoCompare
from ..utils.namespace import Namespace


class BaseStruct(AutoCompare):
    __compare_attrs__ = ('name',)

    def __init__(self, name):
        self.name = name
        self.joins = set()
        self.info = Infomation()


class BaseError(Exception):
    ...


class ObjectExistError(BaseError):
    ...


class Infomation(Namespace):
    ...


class User(BaseStruct):
    def __init__(self, name):
        super().__init__(name)
        self.info = Infomation()


class Group(BaseStruct):
    def __init__(self, name):
        super().__init__(name)
        self.info = Infomation()


class Domain(BaseStruct):
    def __init__(self, name):
        super().__init__(name)
        self.info = Infomation()


priority_dict = {
    "User": 0,
    "Group": 1,
    "Domain": 2,
    User: 0,
    Group: 1,
    Domain: 2
}


class Manager:
    def __init__(self, users=None, groups=None, domains=None):
        self.objects = AutoRegDict()
        if users is not None:
            for user in users:
                self.add_user(user)
        if groups is not None:
            for group in groups:
                self.add_group(group)

        if domains is not None:
            for domain in domains:
                self.add_domain(domain)

    def add_user(self, user: User) -> bool:
        if user.name in self.objects:
            return False
        self.objects[user.name] = user
        return True

    def remove_user(self, user: User) -> bool:
        if user.name not in self.objects:
            return False
        del self.objects[user.name]
        return True

    def add_group(self, group: Group) -> bool:
        if group.name in self.objects:
            return False
        self.objects[group.name] = group
        return True

    def remove_group(self, group: Group) -> bool:
        if group.name not in self.objects:
            return False
        del self.objects[group.name]
        return True

    def add_domain(self, domain: Domain) -> bool:
        if domain.name in self.objects:
            return False
        self.objects[domain.name] = domain
        return True

    def remove_domain(self, domain: Domain) -> bool:
        if domain.name not in self.objects:
            return False
        del self.objects[domain.name]
        return True

    def create_user(self, name):
        if name in self.objects:
            raise ObjectExistError(f"{name} is already exist")
        u = User(name)
        self.objects[name] = u

    def create_group(self, name):
        if name in self.objects:
            raise ObjectExistError(f"{name} is already exist")
        g = Group(name)
        self.objects[name] = g

    def create_domain(self, name):
        if name in self.objects:
            raise ObjectExistError(f"{name} is already exist")
        d = Domain(name)
        self.objects[name] = d

    _ContainerType = Union[Group, Domain]
    _NonTopType = Union[User, Group]

    def let_join(self, name, container):
        nontop_obj = self.objects[name]
        container_obj = self.objects[container]
        if not isinstance(container_obj, self._ContainerType):
            raise TypeError(f'{container_obj} is not a container')
        if not isinstance(nontop_obj, self._NonTopType):
            raise TypeError(f'{nontop_obj} is not a non-top object')
        if priority_dict[type(nontop_obj)] > priority_dict[type(container_obj)]:
            raise TypeError(f'{nontop_obj} is not a {container_obj}')
        # TODO: 完成容器加入操作， 完成容器离开操作
        if container_obj in nontop_obj.joins:
            raise ObjectExistError(f"{nontop_obj} is already in {container_obj}")
        nontop_obj.joins.add(container_obj)

    def let_leave(self, name, container):
        nontop_obj = self.objects[name]
        container_obj = self.objects[container]
        if not isinstance(container_obj, self._ContainerType):
            raise TypeError(f'{container_obj} is not a container')
        if not isinstance(nontop_obj, self._NonTopType):
            raise TypeError(f'{nontop_obj} is not a non-top object')
        if container_obj not in nontop_obj.joins:
            raise ObjectExistError(f"{nontop_obj} is not in {container_obj}")
        nontop_obj.joins.remove(container_obj)

    def get_info(self, name):
        if name not in self.objects:
            return None
        return self.objects[name].info

    def get_obj(self, name):
        return self.objects[name]
