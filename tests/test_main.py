"""Test cases for the __main__ module."""
import pytest
from typer.testing import CliRunner

from galaxies_datasets import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.app, ["--help"])
    assert result.exit_code == 0
