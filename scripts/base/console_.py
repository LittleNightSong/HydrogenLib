import contextlib
import sys

import rich.traceback
from rich import print


class Console:
    _instance: 'Console' = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def error(self, *msg, exit=1):
        print('[red]Error:[/red]', *msg, file=sys.stderr)

        if exit is not None:
            sys.exit(exit)

    def info(self, *msg):
        print('[green]Info:[/green]', *msg)

    def warn(self, *msg):
        print('[yellow]Warning:[/yellow]', *msg)

    def debug(self, *msg):
        print('[gray]Debug:[/gray]', *msg)

    @contextlib.contextmanager
    def status(self, msg, exit_on_error=1, print_reason=True, print_traceback=False):
        try:
            print(msg, '...', end='')
            yield
            print('[green]Success![/green]')
        except Exception as e:
            print("[red][bold]Failed![/bold][/red]", end='')
            if print_reason:
                print(f'\n[red]{e.__class__.__name__}: {e}[/red]', sep='', file=sys.stderr)
            if print_traceback:
                print(file=sys.stderr)
                print(
                    rich.traceback.Traceback.extract(type(e), e, e.__traceback__)
                    , file=sys.stderr)
            if exit_on_error:
                sys.exit(exit_on_error)
            print(file=sys.stderr)

    def print(self, *args, **kwargs):
        return print(*args, **kwargs)


console = Console()
