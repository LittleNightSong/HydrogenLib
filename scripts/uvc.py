import subprocess as sp
from os import PathLike

import uv as _uv

uvexec = _uv.find_uv_bin()


def uv(commands: list | str, cwd=None) -> sp.CompletedProcess:
    return sp.run(
        commands, executable=uvexec, stdout=sp.PIPE, stderr=sp.STDOUT, cwd=cwd, check=True
    )


def build(project_dir: PathLike[str]):
    return uv(["build"], cwd=project_dir)


def install(modules: list[str]):
    return uv(["install", *modules])


def uninstall(modules: list[str]):
    return uv(["uninstall", *modules])
