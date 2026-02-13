import importlib
import importlib.util
import os
import sys


def load_source(path, name=None):
    if name in sys.modules:
        raise ImportError(f"Module {name} already exists in sys.modules")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Cannot find file {path}")

    if name is None:
        name = os.path.basename(path)[:-3]

    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name}(One attribute is None)")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_package(name, path):
    if name in sys.modules:
        raise ImportError(f"Package {name} already exists in sys.modules")

    package_path = os.path.join(path, name)
    if not os.path.exists(package_path):
        raise FileNotFoundError(
            f"Cannot find package {name} at {package_path}")

    init_filename = os.path.join(package_path, "__init__.py")

    if not os.path.exists(init_filename):
        raise FileNotFoundError(
            f"Cannot find __init__.py in package {name}")

    spec = importlib.util.spec_from_file_location(name, init_filename)
    if spec is None:
        raise ImportError(f"Cannot load package {name}(Spec by None)")
    if spec.loader is None:
        raise ImportError(f"Cannot load package {name}(Loader by None)")

    package = importlib.util.module_from_spec(spec)

    sys.modules[name] = package
    spec.loader.exec_module(package)

    return package
