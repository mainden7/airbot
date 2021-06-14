import argparse
import typing as ty

from itertools import tee
from itertools import filterfalse

from airbot.cli.args import Arg
from airbot.cli.args import CLICommand
from airbot.cli.args import GroupCommand
from airbot.cli.args import ALL_COMMANDS_DICT
from airbot.cli.args import ActionCommand

_UNSET = object()


def partition(pred: ty.Callable, iterable: ty.Iterable):
    """
    Use a predicate to partition entries into false entries and true entries
    """
    iter_1, iter_2 = tee(iterable)
    return filterfalse(pred, iter_1), filter(pred, iter_2)


def get_parser() -> argparse.ArgumentParser:
    """Creates and returns command line argument parser"""
    parser = argparse.ArgumentParser(prog="vocab")
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True

    subparser_list = ALL_COMMANDS_DICT.keys()
    sub_name: str
    for sub_name in sorted(subparser_list):
        sub: CLICommand = ALL_COMMANDS_DICT[sub_name]
        _add_command(subparsers, sub)
    return parser


# noinspection PyUnresolvedReferences
def _add_command(
    subparsers: argparse._SubParsersAction, sub: CLICommand
) -> None:
    sub_proc = subparsers.add_parser(
        sub.name,
        help=sub.help,
        description=sub.description or sub.help,
    )
    sub_proc.formatter_class = argparse.RawTextHelpFormatter

    if isinstance(sub, GroupCommand):
        _add_group_command(sub, sub_proc)
    elif isinstance(sub, ActionCommand):
        _add_action_command(sub, sub_proc)
    else:
        raise argparse.ArgumentTypeError("Invalid command definition.")


def _sort_args(args: ty.Iterable[Arg]) -> ty.Iterable[Arg]:
    """
    Sort subcommand optional args, keep positional args
    """

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def get_long_option(arg: Arg):
        """
        Get long option from Arg.flags
        """
        return arg.flags[0] if len(arg.flags) == 1 else arg.flags[1]

    positional, optional = partition(
        lambda x: x.flags[0].startswith("-"), args
    )
    yield from positional
    yield from sorted(optional, key=lambda x: get_long_option(x).lower())


def _add_group_command(
    sub: GroupCommand, sub_proc: argparse.ArgumentParser
) -> None:
    subcommands = sub.subcommands
    sub_subparsers = sub_proc.add_subparsers(dest="subcommand")
    sub_subparsers.required = True

    for command in sorted(subcommands, key=lambda x: x.name):
        _add_command(sub_subparsers, command)


def _add_action_command(
    sub: ActionCommand, sub_proc: argparse.ArgumentParser
) -> None:
    for arg in _sort_args(sub.args):
        arg.add_to_parser(sub_proc)
    sub_proc.set_defaults(func=sub.func)
