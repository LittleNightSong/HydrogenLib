import shutil
import sys

from scripts.base import console, Project
from scripts.commands import uvc, hatchc


def main():
    project = Project()
    # 处理新的版本号
    ver = sys.argv[1] if len(sys.argv) > 1 else None

    if ver:
        with console.status('Setting version'):
            hatchc.set_version(project.path, ver)

    hydrogenlib = project.path / 'hydrogenlib'

    version_info = (hydrogenlib / '__init__.py').read_bytes()

    shutil.rmtree(hydrogenlib, ignore_errors=True)
    hydrogenlib.mkdir(parents=True)

    (hydrogenlib / '__init__.py').write_bytes(version_info)

    for module in project.iter_modules():
        target_reimport_file = hydrogenlib / (module.name.replace('-', '_') + '.py')
        target_reimport_dir = hydrogenlib / (module.name.replace('-', '_'))
        if (re_import_file := (module.path / 're-import.py')).exists():
            shutil.copy(re_import_file, target_reimport_file)
            console.info(f"{f'<{module.name}>':20} Find existing re-import, copy to project dir")
        elif (re_import_dir := (module.path / 're-import')).exists():
            shutil.copytree(re_import_dir, target_reimport_dir)
            console.info(f"{f'<{module.name}>':20} Find existing re-import, copy to project dir")
            if not (_ := target_reimport_dir / '__init__.py').exists():
                console.warn(f'`__init__.py` not found in [bold]{module.name}[/bold]\'s re-import directory')
                _.touch()
        else:
            # 自动生成 re-import
            target_reimport_file.write_text(
                f"from {module.import_name} import *"
            )
            console.info(f"{f'<{module.name}>':20} Generate re-import.py")

    with console.status('Building project'):
        cp = uvc.uv(['build'], cwd=project.path)


if __name__ == '__main__':
    main()
