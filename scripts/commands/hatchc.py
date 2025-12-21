import subprocess as sp

import packaging.version


def hatch(commands, cwd=None):
    return sp.run(
        ["hatch", *commands], stdout=sp.PIPE, stderr=sp.STDOUT, check=True, cwd=cwd
    )


def set_version(module_dir, ver):
    ver = str(ver)
    return hatch(['version', ver], cwd=module_dir)


def get_version(module_dir):
    orginal_ver = hatch(['version'], cwd=module_dir).stdout.decode("utf-8").splitlines()[-1].strip()
    return packaging.version.Version(orginal_ver)
