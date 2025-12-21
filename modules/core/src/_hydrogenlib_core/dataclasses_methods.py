import dataclasses


def default_factory[T](factory: T, **kwargs) -> T:
    return dataclasses.field(default_factory=factory, **kwargs)
