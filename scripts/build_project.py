import shutil
import sys

from scripts.commands import uvc, hatchc
from scripts.base import find_project_dir, console, iter_modules, convert_to_package_name, project_dir


def main():
    # 处理 re-import 文件
    ver = sys.argv[1] if len(sys.argv) > 1 else None

    if ver:
        with console.status('Setting version'):
            hatchc.set_version(project_dir, ver)

    for module in iter_modules():
        target_reiport_file = find_project_dir() / 'hydrogenlib' / (module.name + '.py')
        if (re_import_file := (module / 're-import.py')).exists():
            shutil.copy(re_import_file, target_reiport_file)
            console.info(f"{f'<{module.name}>':20} Find existing re-import.py, copy to project dir")
        else:
            # 手动生成 re-import
            main_package = f"_hydrogenlib_{convert_to_package_name(module.name)}"
            target_reiport_file.write_text(
                f"from {main_package} import *"
            )
            console.info(f"{f'<{module.name}>':20} Generate re-import.py")

    with console.status('Building project'):
        cp = uvc.uv(['build'], cwd=project_dir)


if __name__ == '__main__':
    main()
