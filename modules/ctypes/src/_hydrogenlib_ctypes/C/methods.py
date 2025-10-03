def get_types_from_signature(signature):
    for param in signature.parameters.values():
        yield param.annotation

