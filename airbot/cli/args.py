import os
import argparse
import typing as ty
from airbot.cli.functions import lazy_load_command

_UNSET = object()


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
    default=os.getcwd(),
)

_commands: ty.List[CLICommand] = [
    ActionCommand(
        name="start",
        help=(
            "Participate in all airdrops for specified in configuration file"
            " sources"
        ),
        func=lazy_load_command("airbot.cli.functions", "start"),
        args=(ARG_DIR,),
    )
]

ALL_COMMANDS_DICT: ty.Dict[str, CLICommand] = {sp.name: sp for sp in _commands}
