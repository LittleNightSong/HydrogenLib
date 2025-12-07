import dataclasses
import enum
import json


class CacheControlFlags(str, enum.Enum):
    private = enum.auto()
    public = enum.auto()
    no_cache = enum.auto()
    no_store = enum.auto()
    must_revalidate = enum.auto()
    proxy_revalidate = enum.auto()
    max_age = enum.auto()
    immutable = enum.auto()


@dataclasses.dataclass
class CacheInfo:
    control_flags: set[CacheControlFlags]
    max_age: int | None = None
    expires_in: int | None = None
    vary: str | None = None
    etag: str | None = None

    def to_dict(self):
        return dataclasses.asdict(self)

    def to_json(self):
        return json.dumps(
            self.to_dict()
        )

    def save(self, fp):
        fp.write(self.to_json())

    @classmethod
    def load(cls, fp):
        return cls(**json.loads(fp.read()))
