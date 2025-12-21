from pathlib import Path
import subprocess

bitmap_module_path = Path(__file__).parent.parent.parent / 'data_structures' / 'Bitmap' / '_bitmap'


def main():
    ps = subprocess.run([
        'python.exe',
        str(bitmap_module_path / 'setup.py'),
        'build',
    ], cwd=str(bitmap_module_path.parent), check=True)
