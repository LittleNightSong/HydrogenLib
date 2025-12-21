import os
import re

from packaging.version import Version

import build_project as bp
import subprocess as sp


def quick_extract(dct, *keys):
    for k in keys:
        yield dct[k]


command_finder = re.compile(
    r"\s*# Action:\s*```\s*text\s*(.*?)\s*```",
    re.MULTILINE | re.DOTALL
)


def main():
    tag, title, notes = quick_extract(
        os.environ,
        "RELEASE_TAG", "RELEASE_NAME", "RELEASE_NOTES"
    )

    command_string = command_finder.search(notes).group(1)
    commands = filter(lambda x: x.strip(), command_string.split("\n"))

    generic_args = []

    cmd: str
    for cmd in commands:  # cmd: Name=Version
        package_name, package_version = cmd.split("=")
        # 检查名称合法性
        if not package_name.isidentifier():
            raise ValueError(f"Invalid package name: {package_name}") from None

        try:
            if package_version in {'current', 'patch', 'major', 'minor'}:
                pass  # 这些版本号可以被 hatch version 识别, 但无法被 Version 类识别
            else:
                Version(package_version)  # 检查版本号合法性
        except Exception as e:
            raise e.with_traceback(None)

        generic_args.append(cmd)

    sp.run(
        ['python', './scripts/build_project.py', *generic_args, '--only', '--publish']
    )


if __name__ == '__main__':
    main()
