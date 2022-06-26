import os
import sys
from enum import IntEnum
from functools import partial, wraps

import click


class Console:
    stdout = click.echo
    stderr = partial(click.echo, err=True)


class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1


@click.command(
    options_metavar="[<options>]",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.argument(
    "revision_range",
    metavar="[<revision range>]",
    default="HEAD",
    required=False,
)
def decollator(revision_range):
    """
    Generates a changelog

    <revision range>

        Show only commits in the specified revision range. When no <revision range> is specified,
        it defaults to HEAD (i.e. the whole history leading to the current commit). origin..HEAD specifies all
        the commits reachable from the current commit (i.e.  HEAD), but not from origin.
        For a complete list of ways to spell <revision range>, see the Specifying Ranges section of gitrevisions(7).
    """
    raise NotImplementedError()


def _is_backtrace_enabled():
    """Are stack traces enabled"""
    return os.environ.get("PYTHON_BACKTRACE", None) in ["1", "True", "true"]


def _disable_backtrace(func):
    """Decorator to suppress python stack traces"""

    @wraps(func)
    def catch_all(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            msg = "\n".join(
                (
                    f"Error while executing [{__name__}], details: {str(ex) or '<not available>'}",
                    "To get a full stack trace set PYTHON_BACKTRACE=1",
                )
            )
            Console.stderr(msg)
            sys.exit(ExitCode.FAILURE)

    return catch_all


def main() -> None:
    _main = (
        _disable_backtrace(decollator) if not _is_backtrace_enabled() else decollator
    )
    _main()
