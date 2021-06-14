import os
import argparse
import typing as ty
from importlib import import_module

_UNSET = object()


def lazy_load_command(import_path: str, func: str) -> ty.Callable:
    """Create a lazy loader for command"""
    _, _, name = import_path.rpartition(".")

    def command(*args, **kwargs):
        module = import_module(import_path)
        func_ = getattr(module, func)
        return func_(*args, **kwargs)

    command.__name__ = name

    return command


def find_config():
    dir_ = os.getcwd()
    cf = os.path.join(dir_, "config.ini")
    if os.path.exists(cf):
        return cf
    else:
        raise FileNotFoundError


class Arg:
    """Class to keep information about command line argument"""

    def __init__(
        self,
        flags=_UNSET,
        help=_UNSET,
        action=_UNSET,
        default=_UNSET,
        nargs=_UNSET,
        type=_UNSET,
        choices=_UNSET,
        required=_UNSET,
        metavar=_UNSET,
    ):
        self.flags = flags
        self.kwargs = {}
        for k, v in locals().items():
            if v is _UNSET:
                continue
            if k in ("self", "flags"):
                continue

            self.kwargs[k] = v

    # noinspection PyArgumentList
    def add_to_parser(self, parser: argparse.ArgumentParser):
        """Add this argument to an ArgumentParser"""
        parser.add_argument(*self.flags, **self.kwargs)


class ActionCommand(ty.NamedTuple):
    """Single CLI command"""

    name: str
    help: str
    func: ty.Callable
    args: ty.Iterable[Arg]
    description: ty.Optional[str] = None


class GroupCommand(ty.NamedTuple):
    """ClI command with subcommands"""

    name: str
    help: str
    subcommands: ty.Iterable
    description: ty.Optional[str] = None


CLICommand = ty.Union[ActionCommand, GroupCommand]
ARG_DIR = Arg(
    ("-f", "--config-file"),
    help="Path to the configuration file",
    default=find_config(),
)

_commands: ty.List[CLICommand] = [
    ActionCommand(
        name="start",
        help=(
            "Participate in all airdrops"
        ),
        func=lazy_load_command("airbot.cli.commands", "start"),
        args=(ARG_DIR,),
    )
]

ALL_COMMANDS_DICT: ty.Dict[str, CLICommand] = {sp.name: sp for sp in _commands}
