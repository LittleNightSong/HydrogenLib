import sys
from scripts.base import convert_to_module_name, convert_to_package_name, find_project_dir, find_module
from pathlib import Path


def main():
    module_name = sys.argv[1].lower()
    project_dir = find_project_dir()
    module = find_module(module_name, project_dir)

    uvc.build()



