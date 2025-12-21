from typing import Generator, Callable, overload, Iterator


class EnhancedGenerator[YT, ST, RT](Generator[YT, ST, RT]):

    def throw(self, typ, val=None, tb=None, /):
        ...

    def send(self, value: ST, /) -> YT:
        ...

    def __init__(self, gen: Generator[YT, ST, RT], history: bool = False):
        ...

    def trace(self, val: YT):
        ...

    def next(self, value: ST = None):
        ...

    def next_with_exception(self, exception: Exception) -> YT:
        ...

    def get(self, index: int) -> YT:
        ...

    def iter_slice(self, slice_: slice) -> Iterator[YT]:
        ...

    def iter_n(self, n: int) -> Iterator[YT]:
        ...

    def __getitem__(self, item) -> YT:
        ...


@overload
def enhanced_generator[YT, ST, RT, **P](
        func: Callable[P, Generator[YT, ST, RT]]
) -> Callable[P, EnhancedGenerator[YT, ST, RT]]:
    ...


@overload
def enhanced_generator[YT, ST, RT, **P](
        *,
        history: bool = False
) -> Callable[
    [
        Callable[P, Generator[YT, ST, RT]]
    ],
    Callable[P, EnhancedGenerator[YT, ST, RT]]
]:
    ...
