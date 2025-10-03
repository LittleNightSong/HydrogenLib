import typing

if typing.TYPE_CHECKING:
    from .type_realities import *
    from .impls import Pointer as _Pointer, Ref as _Ref


type Pointer[T] = T | TPointer[T] | _Pointer | TArray | int | None
type Ref[T] = T | TRef[T] | None
type Array[T, N=None] = typing.Sequence[T] | TArray
type ProtoType[RT, *AT] = typing.Callable[[*AT], RT]
