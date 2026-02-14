def make_struct_type[T](name, pytype: type[T], ctype) -> type[T]:
    return type(
        name, (pytype,), {
            '__ctype__': ctype
        }
    )
