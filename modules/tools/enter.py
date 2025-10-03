import sys
import os
from pathlib import Path
from hydrogenlib.core import load_source


def main():
    local = Path(__file__).parent
    scripts = local / 'scripts'

    tool_path = Path(sys.argv[1]).relative_to(scripts)

    if not tool_path.is_relative_to(scripts):
        raise ValueError('Invalid tool path')

    sys.argv.pop(1)
    sys.argv[0] = str(tool_path)

    module = load_source('__hytool__', tool_path)
    module.main()

