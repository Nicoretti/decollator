import pytest

from decollator.cli import (
    ExitCode,
)


def test_cli_constant_success():
    assert ExitCode.SUCCESS == 0


def test_cli_constant_failure():
    assert ExitCode.FAILURE == 1
