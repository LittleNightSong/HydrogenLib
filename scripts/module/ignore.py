import sys

from scripts.base import Project

project = Project()


def main():
    modules = sys.argv[1:]
    reverse = '-r' in modules or '--reverse' in modules
    for module_name in modules:
        if module_name.startswith('-'): continue
        module = project.find_module(module_name, allow_ignored_modules=True, check=False)

        ignore_file = (module.path / '.hydro-ignore')
        if reverse:
            ignore_file.unlink(True)

        else:
            ignore_file.touch()


if __name__ == '__main__':
    main()
