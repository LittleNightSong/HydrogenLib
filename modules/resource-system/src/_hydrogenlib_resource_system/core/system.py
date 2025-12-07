import re
from .provider import ResourceProvider, Resource


class Route:
    _re_matcher = re.compile(r"(/?[a-zA-Z_\-:]*)+")
    def check(self, string: str):
        return self._re_matcher.fullmatch(string)

    def match(self, url) -> bool: ...


class ResourceSystem:
    _name_checker = re.compile(r"[a-zA-Z_\-:@$]+")

    def _check_name(self, name: str):
        result = self._name_checker.fullmatch(name)
        if result is None:
            raise ValueError(f"Invalid name: {name}")

    def __init__(self):
        self._mounttab = {}

    def mount(self, name: str, provider: ResourceProvider):
        self._check_name(name)
        self._mounttab[name] = provider
