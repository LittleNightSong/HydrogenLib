import shutil
import sys

from scripts.base import console, Project


def main():
    project = Project.find()
    modules = sys.argv[1:]
    for m in modules:
        with console.status("Processing %s" % m):
            module = project.find_module(m)
            shutil.rmtree(module.path / 'dist', ignore_errors=True)


if __name__ == "__main__":
    main()
