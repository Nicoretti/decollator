import argparse
from pathlib import Path
from shutil import rmtree

import nox

BASEPATH = Path(__file__).parent.resolve()
DOCS = BASEPATH / "docs"
SRC_DIRECTORY = DOCS
BUILD_DIRECTORY = DOCS / "_build"
INDEX_PAGE = BUILD_DIRECTORY / "html" / "index.html"

nox.options.sessions = [
    "fix",
    "verify",
]


@nox.session(python=False)
def integration(session):
    """Run all integration tests of this project."""
    session.run("poetry", "run", "python", "-m", "prysk", f"{BASEPATH / 'test'}")


@nox.session(python=False)
def doc(session):
    """
    Generate and open the project documentation.

    Usage:
    $ nox -s doc -- [build|open|clean]

    Get Help:
    $ nox -s doc -- -h
    """
    parser = argparse.ArgumentParser(prog="nox -s doc")
    parser.add_argument(
        "action",
        type=str,
        help="The type of action which shall be run.",
        choices={"build", "open", "clean"},
    )

    def _build(s):
        s.run(
            "poetry",
            "run",
            "python",
            "-m",
            "sphinx",
            f"{SRC_DIRECTORY.resolve()}",
            f"{(BUILD_DIRECTORY / 'html').resolve()}",
        )

    def _open(s):
        if not INDEX_PAGE.exists():
            _build(s)
        s.run(
            "python",
            "-m",
            "webbrowser",
            "-t",
            f"{INDEX_PAGE.resolve()}",
        )

    def _clean(s):
        """Remove the build directory."""
        if BUILD_DIRECTORY.exists():
            rmtree(BUILD_DIRECTORY.resolve())
            s.log(f"Removed {BUILD_DIRECTORY}")

    args = parser.parse_args(args=session.posargs)
    dispatcher = {"open": _open, "build": _build, "clean": _clean}
    dispatcher[args.action](session)


@nox.session(python=False)
def ut(session):
    """Run all unit- and doc- tests in this project."""
    session.run("poetry", "run", "python", "-m", "pytest", f"{BASEPATH / 'test'}")


@nox.session(python=False)
def check(session):
    """Run code formatters in check mode."""
    session.run(
        "poetry", "run", "python", "-m", "isort", "-v", "--check", f"{BASEPATH}"
    )
    session.run("poetry", "run", "python", "-m", "black", "--check", f"{BASEPATH}")


@nox.session(python=False)
def fix(session):
    """Run code formatters in fix mode."""
    session.run("poetry", "run", "python", "-m", "isort", "-v", f"{BASEPATH}")
    session.run("poetry", "run", "python", "-m", "black", f"{BASEPATH}")


@nox.session(python=False)
def lint(session):
    """Lint entire project."""
    session.run(
        "poetry", "run", "python", "-m", "pylint", "--recursive=y", f"{BASEPATH}"
    )


@nox.session(python=False)
def typecheck(session):
    """Type check the source code based on the provided type annotations."""
    session.run("poetry", "run", "python", "-m", "mypy", f"{BASEPATH}")


@nox.session(python=False)
def coverage(session):
    """Collect code coverage."""
    session.warn("No Coverage Provided | Details: Not Implemented Yet!")


@nox.session(python=False)
def verify(session):
    """Run a full workspace verification."""
    session.notify("check")
    session.notify("ut")
    session.notify("integration")
    session.notify("lint")
    session.notify("typecheck")
    session.notify("coverage")
