import subprocess as sp
from os import PathLike

import uv as _uv

uvexec = _uv.find_uv_bin()


def uv(commands: list | str, cwd=None) -> sp.CompletedProcess:
    return sp.run(
        [uvexec, *commands], stdout=sp.PIPE, stderr=sp.PIPE, cwd=cwd, check=True
    )


def build(project_dir: PathLike[str] | str):
    return uv(["build"], cwd=project_dir)


def install(modules: list[str]):
    return uv(["install", *modules])


def uninstall(modules: list[str]):
    return uv(["uninstall", *modules])


def publish(module_dir, dist_dir=None):
    c = ["publish"]
    if dist_dir:
        c.append(dist_dir)
    return uv(c, cwd=module_dir)
