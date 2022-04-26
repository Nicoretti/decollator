import pytest

from decollator.cli import FAILURE, SUCCESS


def test_cli_constant_success():
    assert SUCCESS == 0


def test_cli_constant_failure():
    assert FAILURE == -1
