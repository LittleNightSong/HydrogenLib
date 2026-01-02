import tomlkit

from scripts.base import Project, console


def main():
    project = Project()
    for module in project.iter_modules():
        with console.status(f'Updating {module.name}', exit_on_error=False):
            pyproject = module.files.pyproject

            with open(pyproject, 'r') as f:
                toml = tomlkit.load(f)

            toml['project']['authors'] = [
                {
                    'name': 'LittleNightSong',
                    'email': 'LittleNightSongYO@outlook.com'
                }
            ]

            with open(pyproject, 'w') as f:
                tomlkit.dump(toml, f)


if __name__ == '__main__':
    main()
